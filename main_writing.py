import os
import dotenv
import requests
from random import randint


dotenv.load_dotenv()
token = os.environ.get("API_KEY")
server_url = os.environ.get("SERVER_URL")
schema = os.environ.get("SCHEMA")

url = server_url+ "/"+ schema + "/tables/graphql"
headers = {
    "Content-Type": "application/json",
    "x-molgenis-token": token
}

BATCH_SIZE = 1000

names_list = [] #data insterted later
surname_list = []
current_id = 0

    
def main():
    global current_id
    NUMBER_OF_BATCHES_CLIENT = 0
    NUMBER_OF_BATCHES_TICKET = 10
    NUMBER_OF_BATCHES_CLIENT_TICKET = 0
    NUMBER_OF_BATCHES_TEST = 10
    NUMBER_OF_BATCHES_TEST_2 = 10
    NUMBER_OF_BATCHES_TEST_3 = 50
    NUMBER_OF_BATCHES_TEST_4 = 50
    
    table = "Client_table"
    table_params_string = [
        ("id", lambda : str(current_id)),
        ("name", lambda : names_list[randint(0, len(names_list) - 1)]),
        ("surname", lambda : surname_list[randint(0, len(surname_list) - 1)]),
        ("created_on",lambda: "2025-07-01T12:00:00"),
        ("date_of_birth", lambda: str(randint(1950,2024))+"-05-03")
        ]
    table_params_non_string = [
        ("country", lambda: """{name: "Slovenija"}""")
    ]

    for i in range(NUMBER_OF_BATCHES_CLIENT):
        send_http_request(get_query_for_table(table, table_params_string, table_params_non_string))   
    current_id=0


    table = "Ticket_kind"
    table_params_string = [
        ("id", lambda : str(current_id)),
        ("name", lambda : "Ticket"+str(current_id)),
    ]
    table_params_non_string = [
        ("price", lambda : str(randint(1,100))),
        ("valid_for_h", lambda : str(randint(12,10000)))
    ]

    for i in range(NUMBER_OF_BATCHES_TICKET):
        send_http_request(get_query_for_table(table, table_params_string, table_params_non_string))   
    current_id=0

    if BATCH_SIZE*NUMBER_OF_BATCHES_CLIENT-1 > 1 and BATCH_SIZE*NUMBER_OF_BATCHES_TICKET-1 > 1:
        print("\nClient ticket:")
        table = "Client_ticket"
        table_params_string = [
            ("id", lambda : str(current_id)),
            ("activation_time",lambda: "2025-07-01T12:00:00")
        ]
        table_params_non_string = [
            ("price", lambda : str(randint(1,100))),
            ("client", lambda : "{id: \"" + str(randint(1,BATCH_SIZE*NUMBER_OF_BATCHES_CLIENT-1)) + "\" }" ),
            ("ticket", lambda : "{id: \"" + str(randint(1,BATCH_SIZE*NUMBER_OF_BATCHES_TICKET-1)) + "\" }")
        ]

        for i in range(NUMBER_OF_BATCHES_CLIENT_TICKET):
            send_http_request(get_query_for_table(table, table_params_string, table_params_non_string))   
        current_id=0

    if BATCH_SIZE*NUMBER_OF_BATCHES_TICKET-1 > 1:
        print("\nTest:")
        table = "Test"
        table_params_string = [
            ("id", lambda : str(current_id))
        ]
        table_params_non_string = [
            ("test", lambda : "{id: \"" + str(randint(1,BATCH_SIZE*NUMBER_OF_BATCHES_TICKET-1)) + "\" }" )
        ]

        for i in range(NUMBER_OF_BATCHES_TEST):
            send_http_request(get_query_for_table(table, table_params_string, table_params_non_string))   
        current_id=0

    if BATCH_SIZE*NUMBER_OF_BATCHES_TEST-1 > 1:
        print("\nTest2:")
        table = "Test2"
        table_params_string = [
            ("id", lambda : str(current_id))
        ]
        table_params_non_string = [
            ("test", lambda : "{id: \"" + str(randint(1,BATCH_SIZE*NUMBER_OF_BATCHES_TEST-1)) + "\" }" )
        ]

        for i in range(NUMBER_OF_BATCHES_TEST_2):
            send_http_request(get_query_for_table(table, table_params_string, table_params_non_string))   
        current_id=0

    if BATCH_SIZE*NUMBER_OF_BATCHES_TEST_2-1 > 1:
        print("\nTest3:")
        table = "Test3"
        table_params_string = [
            ("id", lambda : str(current_id))
        ]
        table_params_non_string = [
            ("test", lambda : "{id: \"" + str(randint(1,BATCH_SIZE*NUMBER_OF_BATCHES_TEST_2-1)) + "\" }" )
        ]

        for i in range(NUMBER_OF_BATCHES_TEST_3):
            send_http_request(get_query_for_table(table, table_params_string, table_params_non_string))   
        current_id=0

    if BATCH_SIZE*NUMBER_OF_BATCHES_TEST_3-1 > 1:
        print("\nTest4:")
        table = "Test4"
        table_params_string = [
            ("id", lambda : str(current_id))
        ]
        table_params_non_string = [
            ("test", lambda : "{id: \"" + str(randint(1,BATCH_SIZE*NUMBER_OF_BATCHES_TEST_3-1)) + "\" }" )
        ]

        for i in range(NUMBER_OF_BATCHES_TEST_4):
            send_http_request(get_query_for_table(table, table_params_string, table_params_non_string))   
        current_id=0


def send_http_request(query):
    body = {
        "query": query
    }
    response = requests.post(url, headers=headers, json=body)
    print(response.status_code)
    print(response.text)
def get_query_for_table(table_name, table_params_string, table_params_non_string):
    global current_id
    query = "mutation { save ( " +  table_name + ": ["
    for j in range(BATCH_SIZE):
        current_id+=1

        query_fields = []
        
        for index, param in enumerate(table_params_string):
            query_fields.append(param[0] + ": \"" + param[1]() + "\"")

        for index, param in enumerate(table_params_non_string):
            query_fields.append(param[0] + ": " + param[1]())

        query+="{"
        query+=", ".join(query_fields)
        query+="}"

        if (j != BATCH_SIZE-1):
            query+=","
    
    query += "] ) { message status } }"
    
    #print(query)
    return query    
if __name__ == "__main__":
    with open('name_list.txt', 'r') as file:
        for line in file:
            names_list.append(line.strip())
    with open('surname_list.txt', 'r') as file:
        for line in file:
            surname_list.append(line.strip())
    main()  