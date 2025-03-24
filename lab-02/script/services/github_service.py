import os
import shutil
import subprocess

from dotenv import load_dotenv
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

from script.constants.constants import GITHUB_URL, AUTHORIZATION, REPOSITORIES_DIR, FAILED_CLONES_FILE, RESULTS_DIR, STANDART_TIMEOUT
from script.services.csv_service import write_csv, read_csv

QUERY = gql("""
query ($first: Int!, $after: String) {
  search(query: "language:Java stars:>1", type: REPOSITORY, first: $first, after: $after) {
    edges {
      node {
        ... on Repository {
          name
          stargazerCount
          owner {
            login
          }
          createdAt
          updatedAt
          releases {
            totalCount
          }
          url
        }
      }
    }
    pageInfo {
      hasNextPage
      endCursor
    }
  }
}
""")

load_dotenv()


def setup_github_client():
    transport = RequestsHTTPTransport(
        url=GITHUB_URL,
        headers={AUTHORIZATION: f'Bearer {os.getenv("GITHUB_TOKEN")}'},
        use_json=True
    )
    return Client(transport=transport, fetch_schema_from_transport=True)


def fetch_repositories(repositories_count=1000):
    client = setup_github_client()
    has_next = True
    cursor = None
    repositories_fetched = []
    repositories_already_fetched = read_csv("results/repositories.csv")

    if repositories_already_fetched is not None and len(repositories_already_fetched) >= 1000:
        print("Repositories already fetched")
        return

    while has_next and len(repositories_fetched) < repositories_count:
        response = client.execute(QUERY, variable_values={'first': 10 if repositories_count > 10 else repositories_count, 'after': cursor})
        repositories = response['search']['edges']
        page_info = response['search']['pageInfo']
        has_next = page_info['hasNextPage']
        cursor = page_info['endCursor']
        repositories_fetched.extend(repositories)
        print(f"Repositories fetched so far: {len(repositories_fetched)}")

    write_csv(repositories_fetched)

    return repositories_fetched


def clone_repository(repo_url, repo_name, timeout=STANDART_TIMEOUT * 2):
    os.makedirs(REPOSITORIES_DIR, exist_ok=True)
    repo_path = os.path.join(REPOSITORIES_DIR, repo_name)
    failed_clones_path = os.path.join(RESULTS_DIR, FAILED_CLONES_FILE)

    if os.path.exists(repo_path):
        print(f"Repository already exists: {repo_name}")
        return repo_path

    try:
        subprocess.run(["git", "clone", "--depth", "1", "--branch", "main", repo_url, repo_path], stdout=subprocess.DEVNULL,
                       stderr=subprocess.DEVNULL, timeout=timeout)
        if not os.path.exists(repo_path):
            subprocess.run(["git", "clone", "--depth", "1", "--branch", "master", repo_url, repo_path], stdout=subprocess.DEVNULL,
                           stderr=subprocess.DEVNULL, timeout=timeout)

    except subprocess.TimeoutExpired:
        print(f"Failed to clone repository: {repo_name}")
        shutil.rmtree(repo_path, ignore_errors=True)

        if os.path.exists(failed_clones_path):
            with open(failed_clones_path, "r") as log_file:
                failed_repos = {line.strip() for line in log_file}

            if repo_name in failed_repos:
                return None

        with open(failed_clones_path, "a") as log_file:
            log_file.write(f"{repo_name}\n")

        return None

    return repo_path
