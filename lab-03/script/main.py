import os

from script.constants.constants import REPOSITORIES_TO_FETCH, PULL_REQUESTS_TO_FETCH, RESULTS_DIR
from script.services.csv_service import read_csv
from script.services.github_service import fetch_repositories, fetch_repositories_pull_requests


def main():
    fetch_repositories(REPOSITORIES_TO_FETCH)
    fetch_repositories_pull_requests(PULL_REQUESTS_TO_FETCH)
    result = read_csv(os.path.join(RESULTS_DIR, "pull_requests.csv"))
    print(result)

if __name__ == '__main__':
    main()
