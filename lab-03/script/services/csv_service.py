import csv
import os

from script.constants.constants import *


def write_repositories_csv(repositories_fetched, fieldnames, filename, directory=RESULTS_DIR):
    with open(os.path.join(directory, filename), WRITE_COMMAND, newline=EMPTY_STRING, encoding=STANDARD_ENCODING) as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for repo in repositories_fetched:
            repository_data = repo[NODE]
            write_csv(fieldnames, repository_data, writer)


def write_pull_requests_csv(pull_requests_fetched, fieldnames, filename, directory=RESULTS_DIR):
    with open(os.path.join(directory, filename), WRITE_COMMAND, newline=EMPTY_STRING, encoding=STANDARD_ENCODING) as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for repository_name, pull_request_list in pull_requests_fetched.items():
            print('Writing pull requests for repository:', repository_name)
            for pull_request in pull_request_list:
                pull_request_data = pull_request[NODE]
                pull_request_data[REPOSITORY] = repository_name
                write_csv(fieldnames, pull_request_data, writer)


def write_csv(fieldnames, data, writer):
    row = {}
    for field in fieldnames:
        keys = field.split(DOT)
        value = data
        for key in keys:
            value = value.get(key, None)
        row[field] = value
    writer.writerow(row)


def read_csv(path) -> any:
    if os.path.exists(path):
        with open(path, READ_COMMAND, newline=EMPTY_STRING, encoding=STANDARD_ENCODING) as csvfile:
            reader = csv.DictReader(csvfile)
            return [row for row in reader]
    else:
        print("First time running the script. No repositories.csv found.")
