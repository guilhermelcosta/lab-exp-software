import os

from dotenv import load_dotenv
from gql import Client
from gql.transport.requests import RequestsHTTPTransport

from script.constants.constants import *
from script.queries.get_pull_requests_query import FETCH_PULL_REQUESTS_QUERY
from script.queries.get_repositories_query import FETCH_REPOSITORIES_QUERY
from script.services.csv_service import write_repositories_csv, read_csv, write_pull_requests_csv

load_dotenv()


def setup_github_client() -> Client:
    transport = RequestsHTTPTransport(
        url=GITHUB_URL,
        headers={AUTHORIZATION: f'{BEARER} {os.getenv(GITHUB_TOKEN)}'},
        use_json=True
    )
    return Client(transport=transport, fetch_schema_from_transport=True)


def fetch_repositories(repositories_count: int = 1000) -> list:
    client = setup_github_client()
    has_next = True
    cursor = None
    repositories_fetched = []

    if not are_data_fetched(repositories_count, RESULTS_DIR, REPOSITORIES_FILE):
        while has_next and len(repositories_fetched) < repositories_count:
            try:
                response = client.execute(FETCH_REPOSITORIES_QUERY, variable_values={
                    FETCH_RATE: REPOSITORY_FETCH_RATE if repositories_count > REPOSITORY_FETCH_RATE else repositories_count,
                    AFTER: cursor})
            except Exception as e:
                print("Erro while fetching repositories: ", e)
                continue

            repositories = response[SEARCH][EDGES]
            page_info = response[SEARCH][PAGE_INFO]
            has_next = page_info[HAS_NEXT_PAGE]
            cursor = page_info[END_CURSOR]
            repositories_fetched.extend(repositories)
            print(f"Repositories fetched so far: {len(repositories_fetched)}")

        write_repositories_csv(repositories_fetched, REPOSITORY_FIELD_NAMES, REPOSITORIES_FILE)
    else:
        print("Repositories already fetched")

    return repositories_fetched


def fetch_repositories_pull_requests(pull_requests_per_repository: int) -> dict:
    client = setup_github_client()
    repositories = read_csv(os.path.join(RESULTS_DIR, REPOSITORIES_FILE))
    pull_requests_fetched = {}

    for index, repository in enumerate(repositories):
        cursor = None
        pull_requests_fetched[repository[NAME]] = []
        repository_pull_requests = int(repository['pullRequests.totalCount'])

    if not are_data_fetched(pull_requests_per_repository, RESULTS_DIR, REPOSITORIES_FILE):
        while len(pull_requests_fetched[repository[
            NAME]]) < pull_requests_per_repository if pull_requests_per_repository is not None else repository_pull_requests:
            try:
                response = client.execute(FETCH_PULL_REQUESTS_QUERY, variable_values={
                    QUERY: f"repo:{repository[REPOSITORY_FIELD_NAMES[INDEX_TWO]]}/{repository[REPOSITORY_FIELD_NAMES[INDEX_ZERO]]}",
                    FETCH_RATE: min(
                        PULL_REQUEST_FETCH_RATE if repository_pull_requests > PULL_REQUEST_FETCH_RATE else repository_pull_requests,
                        pull_requests_per_repository,
                        PULL_REQUESTS_TO_FETCH - len(pull_requests_fetched[repository[NAME]])),
                    AFTER: cursor
                })
                cursor = response[SEARCH][EDGES][INDEX_ZERO][NODE][PULL_REQUESTS][PAGE_INFO][END_CURSOR]
                pull_requests_fetched[repository[NAME]].extend(response[SEARCH][EDGES][INDEX_ZERO][NODE][PULL_REQUESTS][EDGES])
                print(
                    f"Pull requests fetched for {repository[NAME]} ({index + 1}/{len(repositories)}): {len(pull_requests_fetched[repository[NAME]])}")
            except Exception as e:
                print("Error while fetching pull requests: ", e)
                continue

        write_pull_requests_csv(pull_requests_fetched, PULL_REQUESTS_FIELD_NAMES, PULL_REQUESTS_FILE)
    else:
        print("Pull requests already fetched")

    return pull_requests_fetched


def are_data_fetched(fetch_count: int, directory: str, file: str) -> bool:
    file_path = os.path.join(directory, file)

    return len(read_csv(file_path) or []) >= fetch_count
