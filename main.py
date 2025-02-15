import os
import requests
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

query = gql("""
{
  search(query: "stars:>1", type: REPOSITORY, first: 100) {
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
  }
}
""")


def setup_github_client():
    transport = RequestsHTTPTransport(url='https://api.github.com/graphql',
                                      headers={'Authorization': f'Bearer {GITHUB_TOKEN}'},
                                      use_json=True)

    return Client(transport=transport, fetch_schema_from_transport=True)


def main():
    client = setup_github_client()
    response = client.execute(query)
    print(response)


if __name__ == '__main__':
    main()
