import os
import dotenv
import requests

def main():
    dotenv.load_dotenv()
    token = os.environ.get("API_KEY")
    server_url = os.environ.get("SERVER_URL")
    schema = os.environ.get("SCHEMA")

    url = server_url+"/"+schema + "/tables/graphql"
    headers = {
        "Content-Type": "application/json",
        "x-molgenis-token": token
    }
    #querying everything connected to a client
    query = """
    {
        Ticket_kind { 
            name
            valid_for_h
            tickets_usages{
            client { 
                    name
                    surname
                }
            }
        }
    }"""

    body = {
        "query": query
    }

    response = requests.post(url, headers=headers, json=body)
    print(response.status_code)
    print(response.text)

if __name__ == "__main__":
    main()