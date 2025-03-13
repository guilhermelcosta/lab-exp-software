import os
import csv
import subprocess
from dotenv import load_dotenv
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

load_dotenv()

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
    csv_file = 'java_repositories.csv'
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

def run_ck_analysis(repo_path, output_dir="ck_output"):
    os.makedirs(output_dir, exist_ok=True)
    command = ["java", "-jar", "ck.jar", repo_path]
    print(f"Executando: {' '.join(command)}")  # Debugging do comando
    subprocess.run(command)

    # Imprimir arquivos no diretório de saída para verificar se o CK gerou algo
    print(f"Arquivos no diretório {output_dir}: {os.listdir(output_dir)}")


def summarize_ck_results(output_dir=".", summary_file="ck_summary.csv"):
    ck_file = os.path.join(output_dir, "class.csv")
    if not os.path.exists(ck_file):
        print("Arquivo CK não encontrado!")
        return

    # Abrindo o arquivo 'class.csv' para leitura
    with open(ck_file, "r", encoding="utf-8") as infile:
        reader = csv.DictReader(infile)
        fieldnames = ["class", "cbo", "dit", "lcom"]

        # Cria uma lista para armazenar os dados extraídos
        summary_data = []

        for row in reader:
            # Verifique se os valores não estão vazios ou nulos
            if row["cbo"] and row["dit"] and row["lcom"]:
                summary_data.append({
                    "class": row["class"],
                    "cbo": row["cbo"],
                    "dit": row["dit"],
                    "lcom": row["lcom"]
                })

        # Escrevendo os dados no arquivo de resumo
        with open(summary_file, "w", newline="", encoding="utf-8") as outfile:
            writer = csv.DictWriter(outfile, fieldnames=fieldnames)
            writer.writeheader()  # Escreve o cabeçalho
            writer.writerows(summary_data)  # Escreve os dados extraídos

    print(f"Resumo salvo em {summary_file}")


def main():
    repositories = fetch_repositories()
    write_csv(repositories)
    
    # Clonando o primeiro repositório para teste
    first_repo = repositories[1]['node'] #segundo, na vdd
    repo_path = clone_repository(first_repo['url'], first_repo['name'])
    
    # Rodando análise CK
    run_ck_analysis(repo_path)
    
    # Resumindo resultados
    summarize_ck_results()
    print("Análise CK concluída para um repositório.")


if __name__ == '__main__':
    main()
