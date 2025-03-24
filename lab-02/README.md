# Lab-02: Um Estudo das Características de Qualidade de Sistemas Java

## Descrição

Este projeto realiza uma análise das características de qualidade de código de repositórios Java no GitHub. Ele utiliza a API GraphQL do
GitHub para coletar dados dos repositórios e a ferramenta [CK](https://github.com/mauricioaniche/ck) para extrair métricas de qualidade de
código. Além disso, são geradas visualizações gráficas das métricas coletadas.

## Como Executar

### 1. Defina um Token de Autenticação do GitHub

Para acessar a API do GitHub, é necessário um token de autenticação. Configure uma variável de ambiente com o seguinte comando:

```bash
export GITHUB_TOKEN=seu_token_aqui
```  

Substitua `seu_token_aqui` pelo seu token de autenticação pessoal do GitHub.

### 2. Instale as Dependências

As bibliotecas necessárias estão listadas no arquivo `requirements.txt`. Para instalá-las, execute:

```bash
pip install -r requirements.txt
```  

### 3. Execute o Script de Coleta e Análise

Para iniciar a coleta dos dados e a análise das métricas CK, execute o seguinte comando:

```bash
python lab-01/main.py
```  

Esse script:

1. Consulta a API do GitHub para obter informações sobre repositórios Java populares.
2. Clona os repositórios coletados.
3. Executa a ferramenta CK para extrair métricas de qualidade.
4. Salva os resultados em arquivos `.csv` dentro do diretório `results/ck_results`.
5. Gera um resumo das métricas coletadas.

### 4. Gerar Gráficos e Análises

Após a execução do script principal, é possível visualizar os dados gerados executando o script de análise:

```bash
python lab-01/analyze.py
```  

Isso gerará gráficos para visualizar as métricas CK, incluindo dispersão entre CBO e DIT, distribuição de CBO e a média das métricas
extraídas.

## Explicação do Código

- **Coleta de Repositórios:** O código utiliza a API GraphQL do GitHub para buscar repositórios Java com mais de uma estrela. As informações
  coletadas incluem nome, número de estrelas, dono, data de criação e atualização, número de releases e URL do repositório.
- **Processamento dos Repositórios:** Cada repositório é clonado localmente e analisado com a ferramenta CK, que extrai métricas como
  acoplamento (CBO), profundidade da hierarquia de herança (DIT) e falta de coesão (LCOM).
- **Armazenamento e Análise:** Os dados são salvos em arquivos CSV e um resumo é gerado para facilitar a análise posterior.
- **Geração de Gráficos:** O script de análise utiliza `matplotlib` e `seaborn` para criar visualizações das métricas coletadas.

## Considerações

- O script coleta até 1000 repositórios, mas esse número pode ser ajustado no parâmetro `repositories_count` na função `fetch_repositories`.
- A execução do CK pode levar algum tempo dependendo do número de repositórios coletados.
- Certifique-se de que o [Java](https://www.oracle.com/java/technologies/downloads/) está instalado para executar a ferramenta CK
  corretamente.