import os
import dotenv
import requests

dotenv.load_dotenv()
token = os.environ.get("API_KEY")
server_url = os.environ.get("SERVER_URL")
schema = os.environ.get("SCHEMA")

url = server_url+"/"+schema + "/tables/graphql"
headers = {
    "Content-Type": "application/json",
    "x-molgenis-token": token
}

def main():
    query = """
    {
    Client_table { 
        name
        surname
        date_of_birth
        created_on
            country{name}
            activated_tickets  {
            price
            activation_time
            ticket {
                name
                valid_for_h
                price
            }
        }
    }
    }"""
    send_http_request(query)

def send_http_request(query):
    body = {
        "query": query
    }
    response = requests.post(url, headers=headers, json=body)
    print(response.status_code)
    print(response.text)

if __name__ == "__main__":
    main()