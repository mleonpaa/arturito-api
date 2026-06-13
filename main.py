import requests
import yaml

def main():
    print("Hello from arturito-api!")

    url = "http://localhost:8000/agents"
    
    with open("/workspace/arturito-api/config.yaml", "r") as f:
        config= yaml.safe_load(f)
    

    # Use the 'json' parameter to automatically serialize the dict and set proper headers
    response = requests.post(url, json=config)

    if response.status_code == 200:
        result = response.json()
        print(result)
    else:
        print(f"Error {response.status_code}: {response.text}")

if __name__ == "__main__":
    main()
