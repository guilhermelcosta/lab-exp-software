# Lab-01: Características de Repositórios Populares

## Descrição

O código presente no *Lab-01* utiliza a API GraphQL do GitHub para buscar informações sobre repositórios populares (
aqueles com mais de uma estrela). As informações coletadas incluem:

- Nome do repositório
- Quantidade de estrelas
- Proprietário
- Datas de criação e atualização
- Linguagem principal
- Quantidade de pull requests abertos e mesclados
- Número de releases
- Quantidade de issues abertas e fechadas

Esses dados são armazenados em um arquivo `.csv` para análise posterior.

## Como Executar

### 1. Defina um Token de Autenticação do GitHub

Para acessar a API do GitHub, você precisará de um token de autenticação. Defina uma variável de ambiente para o token
com o seguinte comando:

```bash
export GITHUB_TOKEN=seu_token_aqui
```

Substitua `seu_token_aqui` pelo seu token de autenticação pessoal do GitHub.

### 2. Instale as Dependências Necessárias

O código depende de algumas bibliotecas Python. Instale-as usando o `pip`:

```bash
pip install gql requests python-dotenv
```

### 3. Execute o Script

Para executar o script e começar a coletar os dados, execute o seguinte comando:

```bash
python lab-01/main.py
```

Isso fará com que o script consulte a API do GitHub, busque informações sobre os repositórios populares e armazene esses
dados em um arquivo chamado `repositories.csv`.

## Explicação do Código

- **Configuração do Cliente GitHub**: O código utiliza a biblioteca `gql` para se comunicar com a API GraphQL do GitHub.
  O token de autenticação é lido de uma variável de ambiente definida no arquivo `.env`.

- **Consulta GraphQL**: A consulta busca repositórios que tenham mais de uma estrela e coleta várias informações sobre
  cada repositório, incluindo o número de pull requests abertos e mesclados, o número de releases, e as issues abertas e
  fechadas.

- **Gravação no CSV**: O script salva os dados coletados em um arquivo `.csv`, com as informações de cada repositório
  organizadas em colunas.

## Considerações

- O script consulta até 1000 repositórios, mas você pode modificar o parâmetro `repositories_count` na função
  `fetch_repositories` para ajustar esse número.