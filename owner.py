import os
import requests
from typing import Tuple
from dotenv import load_dotenv


# Custom exception for GitHub API errors
class GitHubAPIError(Exception):
    """Exception raised when GitHub API query fails"""
    pass


# Load environment variables from .env file
load_dotenv()

# GitHub API token and username
ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN')
if not ACCESS_TOKEN:
    raise ValueError("ACCESS_TOKEN environment variable is required but not set")

USER_NAME = os.environ.get('USER_NAME')
if not USER_NAME:
    raise ValueError("USER_NAME environment variable is required but not set")

# GitHub GraphQL API endpoint
GRAPHQL_URL = "https://api.github.com/graphql"

def get_owner_id(username: str) -> Tuple[str, str]:
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
        raise GitHubAPIError(f"Query failed with status code {response.status_code}: {response.text}")

if __name__ == "__main__":
    try:
        owner_id, creation_date = get_owner_id(USER_NAME)
        print(f"OWNER_ID: {owner_id}")
        print(f"Account Creation Date: {creation_date}")
    except Exception as e:
        print(f"Error: {e}")