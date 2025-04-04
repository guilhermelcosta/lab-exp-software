import os

from script.constants.constants import REPOSITORIES_DIR, STANDART_TIMEOUT
from script.services.ck_service import run_analysis, summarize_analysis
from script.services.csv_service import read_csv
from script.services.github_service import fetch_repositories, clone_repository
from script.services.graph_service import generate_graphs


def main():
    fetch_repositories()

    repositories = read_csv(os.path.join(REPOSITORIES_DIR))

    for index, repo in enumerate(repositories):
        print(f"Cloning repository: {index + 1}/{len(repositories)}: {repo['name']}")
        clone_repository(repo['url'], repo['name'], STANDART_TIMEOUT)

    run_analysis()
    summarize_analysis()
    generate_graphs()

if __name__ == '__main__':
    main()
