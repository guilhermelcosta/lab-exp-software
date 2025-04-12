from gql import gql

FETCH_PULL_REQUESTS_QUERY = gql("""
query ($query: String!, $fetchRate: Int!, $after: String) {
  search(query: $query, type: REPOSITORY, first: $fetchRate) {
    edges {
      node {
        ... on Repository {
          name,
          pullRequests(states: [MERGED, CLOSED], first: $fetchRate, after: $after) {
            edges {
              node {
                title
                createdAt
                merged
                mergedAt
                closed
                closedAt
                bodyText
                additions
                deletions
                participants(first: 100) {
                  totalCount
                }
                comments(first: 100) {
                  totalCount
                }
                files(first: 100) {
                  totalCount
                }
              }
            }
            pageInfo {
              hasNextPage
              endCursor
            }
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
