from script.constants.constants import REPOSITORIES_TO_FETCH, PULL_REQUESTS_TO_FETCH
from script.services.github_service import fetch_repositories, fetch_repositories_pull_requests


def main():
    fetch_repositories(REPOSITORIES_TO_FETCH)
    fetch_repositories_pull_requests(PULL_REQUESTS_TO_FETCH)


if __name__ == '__main__':
    main()
