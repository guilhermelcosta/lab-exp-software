# Lab-01: Características de Repositórios Populares

## Descrição

O código presente em lab-01 utiliza a API GraphQL do GitHub para buscar repositórios populares (com mais de uma estrela). Ele coleta
informações como:

- Nome do repositório
- Quantidade de estrelas
- Proprietário
- Datas de criação e atualização
- Linguagem principal
- Quantidade de pull requests abertos e mesclados
- Número de releases
- Quantidade de issues abertas e fechadas

## Como Executar

### Defina um token de autenticação do GitHub:

```bash
export TOKEN=seu_token_aqui
```

### Instale as dependências necessárias:

```bash
pip install gql requests
```

### Execute o script:

```bash
python lab-01/main.py
```