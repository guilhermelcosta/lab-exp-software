from gql import gql

FETCH_REPOSITORIES_QUERY = gql("""
query ($fetchRate: Int!, $after: String) {
  search(query: "stars:>1", type: REPOSITORY, first: $fetchRate, after: $after) {
    edges {
      node {
        ... on Repository {
          name,
          url,
          stargazerCount
          owner {
            login
          },
          pullRequests(states: [MERGED, CLOSED]) {
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
