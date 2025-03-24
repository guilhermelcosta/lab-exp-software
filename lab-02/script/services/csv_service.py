import csv
import os

from script.constants.constants import RESULTS_DIR, REPOSITORIES_FILE


def write_csv(repositories_fetched):
    csv_file = os.path.join(RESULTS_DIR, REPOSITORIES_FILE)
    fieldnames = ['name', 'stargazerCount', 'owner', 'createdAt', 'updatedAt', 'releases', 'url']

    with open(csv_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for repo in repositories_fetched:
            repo_data = repo['node']
            writer.writerow({
                'name': repo_data['name'],
                'stargazerCount': repo_data['stargazerCount'],
                'owner': repo_data['owner']['login'],
                'createdAt': repo_data['createdAt'],
                'updatedAt': repo_data['updatedAt'],
                'releases': repo_data['releases']['totalCount'],
                'url': repo_data['url']
            })


def read_csv(path):
    if os.path.exists(path):
        with open(path, 'r', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            return [row for row in reader]
    else:
        print("First time running the script. No repositories.csv found.")
