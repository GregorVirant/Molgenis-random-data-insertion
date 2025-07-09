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
NUMBER_OF_BATCHES = 5

names_list = [] #data insterted later
surname_list = []
current_id = 0

    
def main():
    table = "Client_table"
    table_params_string = [
        ("id", lambda : str(current_id)),
        ("name", lambda : names_list[randint(0, len(names_list) - 1)]),
        ("surname", lambda : surname_list[randint(0, len(names_list) - 1)]),
        ("created_on",lambda: "2025-07-01T12:00:00"),
        ("date_of_birth", lambda: str(randint(1950,2024))+"-05-03")
        ]
    table_params_non_string = [
        ("country", lambda: """{name: "Slovenija"}""")
    ]

    for i in range(NUMBER_OF_BATCHES):
        send_http_request(get_query_for_table(table, table_params_string, table_params_non_string))   

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

        query+="{"
        for index, param in enumerate(table_params_string):
            query += param[0] + ": \"" + param[1]() + "\""
            if (index != len(table_params_string) -1 or len(table_params_non_string) == 0):
                query+=","

        for index, param in enumerate(table_params_non_string):
            query += param[0] + ": " + param[1]()
            if (index != len(table_params_non_string) -1):
                query+=","

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