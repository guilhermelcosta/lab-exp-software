import os
from http.client import responses

from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

query = gql("""
{
  search(query: "stars:>1", type: REPOSITORY, first: 10) {
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
            'Authorization': f'Bearer TOKEN'},
        use_json=True
    )
    return Client(transport=transport, fetch_schema_from_transport=True)


def fetch_repositories(repositories_count=1000):
    client = setup_github_client()
    has_next = True
    cursor = None
    repositories_fetched = []

    while has_next and len(repositories_fetched) <= repositories_count:
        response = client.execute(query, variable_values={'first': 10, 'after': cursor})
        repositories = response['search']['edges']
        page_info = response['search']['pageInfo']
        has_next = page_info['hasNextPage']
        cursor = page_info['endCursor']
        repositories_fetched.extend(repositories)

    return repositories_fetched


def main():
    print(fetch_repositories(20))


if __name__ == '__main__':
    main()
