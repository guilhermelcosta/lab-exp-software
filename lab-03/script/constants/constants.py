# General config
STANDARD_TIMEOUT = 60
INDEX_ZERO = 0
INDEX_ONE = 1
INDEX_TWO = 2
INDEX_THREE = 3
INDEX_FOUR = 4
EMPTY_STRING = ""
STANDARD_ENCODING = "utf-8"
DOT = "."

# CSV config
WRITE_COMMAND = "w"
READ_COMMAND = "r"

# Repository setup
REPOSITORY_FIELD_NAMES = ["name", "stargazerCount", "owner.login", "pullRequests.totalCount", "url"]
PULL_REQUESTS_FIELD_NAMES = ["repository","title", "createdAt", "merged", "mergedAt", "closed", "closedAt", "bodyText", "additions", "deletions",
                             "participants.totalCount", "comments.totalCount", "files.totalCount"]

# Github config
GITHUB_TOKEN = "GITHUB_TOKEN"
GITHUB_URL = "https://api.github.com/graphql"
AUTHORIZATION = "Authorization"
BEARER = "Bearer"
REPOSITORY="repository"
REPOSITORY_FETCH_RATE = 10
PULL_REQUEST_FETCH_RATE = 100
REPOSITORIES_TO_FETCH = 1
PULL_REQUESTS_TO_FETCH = 1
FETCH_RATE = "fetchRate"
AFTER = "after"
REPO = "repo"
NAME = "name"
QUERY = "query"
SEARCH = "search"
EDGES = "edges"
NODE = "node"
PULL_REQUESTS = "pullRequests"
PAGE_INFO = "pageInfo"
HAS_NEXT_PAGE = "hasNextPage"
END_CURSOR = "endCursor"
LOGIN = "login"
TOTAL_COUNT = "totalCount"

# Directories
RESULTS_DIR = "results"
REPOSITORIES_DIR = "repositories"

# Files
REPOSITORIES_FILE = "repositories.csv"
PULL_REQUESTS_FILE = "pull_requests.csv"
FAILED_CLONES_FILE = "failed_clones.csv"
