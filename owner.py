import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# GitHub API token and username
ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN')
USER_NAME = os.environ.get('USER_NAME')

# GitHub GraphQL API endpoint
GRAPHQL_URL = "https://api.github.com/graphql"

def get_owner_id(username):
    """
    Fetches the GitHub account ID and creation date for the given username.
    """
    query = '''
    query($login: String!) {
        user(login: $login) {
            id
            createdAt
        }
    }
    '''
    variables = {"login": username}
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}

    response = requests.post(GRAPHQL_URL, json={"query": query, "variables": variables}, headers=headers)

    if response.status_code == 200:
        data = response.json()
        user_id = data['data']['user']['id']
        created_at = data['data']['user']['createdAt']
        return user_id, created_at
    else:
        raise Exception(f"Query failed with status code {response.status_code}: {response.text}")

if __name__ == "__main__":
    try:
        owner_id, creation_date = get_owner_id(USER_NAME)
        print(f"OWNER_ID: {owner_id}")
        print(f"Account Creation Date: {creation_date}")
    except Exception as e:
        print(f"Error: {e}")