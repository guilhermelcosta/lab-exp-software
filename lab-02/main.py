import os
import csv
import subprocess
from dotenv import load_dotenv
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

load_dotenv()

# Diretórios de saída
RESULTS_DIR = "results"
CK_RESULTS_DIR = os.path.join(RESULTS_DIR, "ck_results")
os.makedirs(CK_RESULTS_DIR, exist_ok=True)

query = gql("""
query ($first: Int!, $after: String) {
  search(query: "language:Java stars:>1", type: REPOSITORY, first: $first, after: $after) {
    edges {
      node {
        ... on Repository {
          name
          stargazerCount
          owner {
            login
          }
          createdAt
          updatedAt
          releases {
            totalCount
          }
          url
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

def setup_github_client():
    transport = RequestsHTTPTransport(
        url='https://api.github.com/graphql',
        headers={'Authorization': f'Bearer {os.getenv("GITHUB_TOKEN")}'},
        use_json=True
    )
    return Client(transport=transport, fetch_schema_from_transport=True)

def write_csv(repositories_fetched):
    csv_file = os.path.join(RESULTS_DIR, 'java_repositories.csv')
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

def fetch_repositories(repositories_count=10):
    client = setup_github_client()
    has_next = True
    cursor = None
    repositories_fetched = []

    while has_next and len(repositories_fetched) < repositories_count:
        response = client.execute(query, variable_values={'first': 10, 'after': cursor})
        repositories = response['search']['edges']
        page_info = response['search']['pageInfo']
        has_next = page_info['hasNextPage']
        cursor = page_info['endCursor']
        repositories_fetched.extend(repositories)
        print(f"Repositórios coletados até agora: {len(repositories_fetched)}")

    return repositories_fetched

def clone_repository(repo_url, repo_name):
    os.makedirs("repositories", exist_ok=True)
    repo_path = os.path.join("repositories", repo_name)
    if not os.path.exists(repo_path):
        subprocess.run(["git", "clone", repo_url, repo_path])
    return repo_path

def run_ck_analysis(repo_path):
    # Executa o CK
    command = ["java", "-jar", "ck.jar", repo_path]
    print(f"Executando: {' '.join(command)}")
    subprocess.run(command)

    # Mover arquivos CK gerados para results/ck_results
    ck_files = ["class.csv", "method.csv", "field.csv", "variable.csv"]
    for file in ck_files:
        src_path = file  # Arquivos são gerados na raiz do script
        dest_path = os.path.join(CK_RESULTS_DIR, file)
        if os.path.exists(src_path):
            os.rename(src_path, dest_path)
            print(f"Movido {file} para {CK_RESULTS_DIR}")
        else:
            print(f"Arquivo {file} não encontrado após a execução do CK.")

def summarize_ck_results():
    class_csv_path = os.path.join(CK_RESULTS_DIR, "class.csv")
    summary_path = os.path.join(CK_RESULTS_DIR, "ck_summary.csv")

    if not os.path.exists(class_csv_path):
        print("Arquivo class.csv não encontrado para resumo!")
        return

    with open(class_csv_path, "r", encoding="utf-8") as infile:
        reader = csv.DictReader(infile)
        fieldnames = ["class", "cbo", "dit", "lcom"]

        summary_data = []

        for row in reader:
            if row["cbo"] and row["dit"] and row["lcom"]:
                summary_data.append({
                    "class": row["class"],
                    "cbo": row["cbo"],
                    "dit": row["dit"],
                    "lcom": row["lcom"]
                })

        with open(summary_path, "w", newline="", encoding="utf-8") as outfile:
            writer = csv.DictWriter(outfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(summary_data)

    print(f"Resumo salvo em {summary_path}")

def main():
    repositories = fetch_repositories()
    write_csv(repositories)
    
    first_repo = repositories[1]['node']
    repo_path = clone_repository(first_repo['url'], first_repo['name'])
    
    run_ck_analysis(repo_path)
    
    summarize_ck_results()
    print("Análise CK concluída para um repositório.")

if __name__ == '__main__':
    main()
