import os
import dotenv
import requests
import time

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
        Ticket_kind {
            id
            test_conn {
                id
                test2b {
                    id
                    test3b {
                        id
                        test4b {
                            id
                        }
                    }
                }
            }
        }
    }
    """
    start_time = time.time()
    send_http_request(query)
    end_time = time.time()

    elapsed = end_time - start_time
    print(f"\nRequired time: {elapsed}")

def send_http_request(query):
    body = {
        "query": query
    }
    response = requests.post(url, headers=headers, json=body)
    print(response.status_code)
    #print(response.text)

if __name__ == "__main__":
    main()