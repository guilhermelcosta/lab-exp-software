import os
import csv
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

query = gql(""" 
query ($first: Int!, $after: String) { 
  search(query: "stars:>1", type: REPOSITORY, first: $first, after: $after) { 
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
          languages(first: 1) { 
            nodes { 
              name 
            } 
          } 
          openPullRequests: pullRequests(states: OPEN) { 
            totalCount 
          } 
          mergedPullRequests: pullRequests(states: MERGED) { 
            totalCount 
          } 
          releases { 
            totalCount 
          } 
          openIssues: issues(states: OPEN) { 
            totalCount 
          } 
          closedIssues: issues(states: CLOSED) { 
            totalCount 
          } 
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

def setup_github_client():
    transport = RequestsHTTPTransport(
        url='https://api.github.com/graphql',
        headers={
            'Authorization': f'Bearer YOUR_GITHUB_TOKEN_HERE'},
        use_json=True
    )
    return Client(transport=transport, fetch_schema_from_transport=True)

def fetch_repositories(repositories_count=1000):
    client = setup_github_client()
    has_next = True
    cursor = None
    repositories_fetched = []

    csv_file = 'repositories.csv'
    
    with open(csv_file, 'a', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['name', 'stargazerCount', 'owner', 'createdAt', 'updatedAt', 'language', 'openPullRequests', 
                      'mergedPullRequests', 'releases', 'openIssues', 'closedIssues']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        if os.stat(csv_file).st_size == 0:
            writer.writeheader()

        while has_next and len(repositories_fetched) < repositories_count:
            response = client.execute(query, variable_values={'first': 10, 'after': cursor})
            repositories = response['search']['edges']
            page_info = response['search']['pageInfo']
            has_next = page_info['hasNextPage']
            cursor = page_info['endCursor']
            repositories_fetched.extend(repositories)

            for repo in repositories:
                repo_data = repo['node']
                writer.writerow({
                    'name': repo_data['name'],
                    'stargazerCount': repo_data['stargazerCount'],
                    'owner': repo_data['owner']['login'],
                    'createdAt': repo_data['createdAt'],
                    'updatedAt': repo_data['updatedAt'],
                    'language': repo_data['languages']['nodes'][0]['name'] if repo_data['languages']['nodes'] else "Unknown",
                    'openPullRequests': repo_data['openPullRequests']['totalCount'],
                    'mergedPullRequests': repo_data['mergedPullRequests']['totalCount'],
                    'releases': repo_data['releases']['totalCount'],
                    'openIssues': repo_data['openIssues']['totalCount'],
                    'closedIssues': repo_data['closedIssues']['totalCount']
                })

            print(f"Fetched {len(repositories_fetched)} repositories so far.")

    return repositories_fetched

def main():
    fetch_repositories(1000)

if __name__ == '__main__':
    main()
