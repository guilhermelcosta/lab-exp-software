import csv
import os
import statistics
import subprocess

from script.constants.constants import RESULTS_DIR, CK_RESULTS_DIR, CK_GENERATED_FILES, REPOSITORIES_DIR, STANDART_TIMEOUT, SUMMARY_CK_FILE, \
    REPOSITORIES_FILE


def run_analysis(repo_path=None, timeout=STANDART_TIMEOUT):
    repositories = [os.path.join(REPOSITORIES_DIR, repo) for repo in os.listdir(REPOSITORIES_DIR)] if repo_path is None else [repo_path]

    os.makedirs(os.path.join(RESULTS_DIR, CK_RESULTS_DIR), exist_ok=True)

    for index, repository in enumerate(repositories):
        repository_name = repository.split("/")[1]
        print(f"Analyzing repository ({index + 1}/{len(repositories)}): {repository_name}")
        command = ["java", "-jar", "ck.jar", repository]

        try:
            subprocess.run(command, stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL, timeout=timeout)

            for file in CK_GENERATED_FILES:
                current_path = file
                destination_path = os.path.join(RESULTS_DIR, CK_RESULTS_DIR, repository_name + "_" + file)

                if os.path.exists(current_path):
                    os.rename(current_path, destination_path)
        except subprocess.TimeoutExpired:
            print(f"Error analyzing repository {repository_name}. Timeout expired.")
            continue

    summarize_analysis()


def summarize_analysis():
    current_ck_results_path = os.path.join(RESULTS_DIR, CK_RESULTS_DIR)
    csv_file = os.path.join(RESULTS_DIR, SUMMARY_CK_FILE)
    repositories_csv_file = os.path.join(RESULTS_DIR, REPOSITORIES_FILE)

    if not os.path.exists(current_ck_results_path):
        return

    file_list = sorted(os.listdir(current_ck_results_path))
    fieldnames = ['repository_name', 'stargazer_count', 'created_at', 'updated_at', 'release_count', 'cbo_average', 'dit_average',
                  'lcom_average', 'cbo_median', 'dit_median', 'lcom_median']

    repo_data_dict = load_repository_data(repositories_csv_file)

    with open(csv_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for index, file in enumerate(file_list):
            repository_name, file_type = parse_file_name(file)
            if file_type == "class":
                print(f"Reading file ({index + 1}/{len(file_list)}): {file}")

                if repository_name in repo_data_dict:
                    value = repo_data_dict[repository_name]
                    write_summary(writer, repository_name, value, os.path.join(current_ck_results_path, file))


def load_repository_data(repositories_csv_file):
    repo_data_dict = {}
    with open(repositories_csv_file, "r", encoding="utf-8") as repo_file:
        repo_reader = csv.DictReader(repo_file)
        for row in repo_reader:
            repo_data_dict[row["name"]] = row
    return repo_data_dict


def parse_file_name(file):
    file_array = file.split(".csv")[0].split("_")
    repository_name = file_array[0]
    file_type = file_array[1]
    return repository_name, file_type


def write_summary(writer, repository_name, value, file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        rows = list(reader)

        if not rows:
            print(f"File {file_path} is empty.")
            return

        header = rows[0]
        try:
            cbo_index = header.index("cbo")
            dit_index = header.index("dit")
            lcom_index = header.index("lcom")
        except ValueError as e:
            print(f"Error locating columns in file {file_path}: {e}")
            return

        # Filtra e converte os valores numéricos corretamente
        cbo_values = [int(row[cbo_index]) for row in rows[1:] if row[cbo_index].isdigit()]
        dit_values = [int(row[dit_index]) for row in rows[1:] if row[dit_index].isdigit()]
        lcom_values = [int(row[lcom_index]) for row in rows[1:] if row[lcom_index].isdigit()]

        # Calcula média e mediana para cada métrica
        cbo_average = sum(cbo_values) / len(cbo_values) if cbo_values else 0
        dit_average = sum(dit_values) / len(dit_values) if dit_values else 0
        lcom_average = sum(lcom_values) / len(lcom_values) if lcom_values else 0

        cbo_median = statistics.median(cbo_values) if cbo_values else 0
        dit_median = statistics.median(dit_values) if dit_values else 0
        lcom_median = statistics.median(lcom_values) if lcom_values else 0

        writer.writerow({
            'repository_name': repository_name,
            'stargazer_count': value["stargazerCount"],
            'created_at': value["createdAt"],
            'updated_at': value["updatedAt"],
            'release_count': value["releases"],
            'cbo_average': cbo_average,
            'cbo_median': cbo_median,
            'dit_average': dit_average,
            'dit_median': dit_median,
            'lcom_average': lcom_average,
            'lcom_median': lcom_median,
        })
