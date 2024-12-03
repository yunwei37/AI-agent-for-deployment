import os
import sys
import json
from dotenv import load_dotenv
import requests

# Load environment variables from .env file
load_dotenv()

def tavily_search(query) -> str:
    url = "https://api.tavily.com/search"
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "api_key": os.getenv("TAVILY_API_KEY"),
        "query": query
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        return response.text
    else:
        raise Exception(f"Request failed with status code {response.status_code}: {response.text}")

def main():
    if len(sys.argv) != 3:
        print("Usage: python tavily_search.py <input_file> <output_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    try:
        with open(input_file, 'r') as f:
            query = f.read().strip()

        response = tavily_search(query)

        with open(output_file, 'w') as f:
            json.dump(response, f, indent=2)

        print(f"Search results saved to {output_file}")

    except FileNotFoundError:
        print(f"Error: Input file '{input_file}' not found.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
