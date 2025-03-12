# Relatório laboratório 2

## Objetivos do relatório

o objetivo deste laboratório é analisar aspectos da qualidade de repositórios desenvolvidos na linguagem Java, correlacionando-os com características do seu processo de desenvolvimento, sob a perspectiva de métricas de produto calculadas através da ferramenta CK. Buscamos analisar:

- RQ 01: Relação entre a popularidade dos repositórios e as suas características de qualidade.
- RQ 02: Relação entre a maturidade do repositórios e as suas características de qualidade.
- RQ 03: Relação entre a atividade dos repositórios e as suas características de qualidade.
- RQ 04: Relação entre o tamanho dos repositórios e as suas características de qualidade.

## Metodologia (COMPLETAR DAQUI PRA BAIXO)

A metodologia adotada para responder às questões de pesquisa será baseada na coleta de dados dos 1.000 repositórios mais
populares do GitHub, utilizando a API GraphQL do GitHub. O processo será dividido em duas etapas:

1. Coleta de Dados

A coleta de dados será realizada por uma consulta GraphQL personalizada para obter informações sobre os 1.000
repositórios mais populares no GitHub. Para isso, será necessário:

- Consulta GraphQL: Desenvolver uma consulta para buscar informações sobre o nome do repositório, número de estrelas,
  proprietário, datas de criação e atualização, linguagem principal, quantidade de pull requests abertos e mesclados,
  número de releases e issues abertas e fechadas.
- Paginação: Para coletar dados de todos os 1.000 repositórios, implementaremos a funcionalidade de paginação na
  consulta
  GraphQL.
- Armazenamento em CSV: Os dados serão armazenados num arquivo .csv para facilitar a análise posterior.

2. Análise dos Dados

Após a coleta dos dados, será realizada a análise para responder às questões de pesquisa:

- Análise Quantitativa: Será calculado o valor médio ou mediano das métricas para cada questão de pesquisa (RQ), como
  idade do repositório, número de pull requests, total de releases, e outros. Essas métricas serão comparadas entre
  diferentes repositórios e linguagens.
- Análise Qualitativa: Para as métricas de categoria, como a linguagem primária dos repositórios, será realizada uma
  contagem para identificar quais linguagens são mais comuns entre os repositórios populares.

## Resultados obtidos

**RQ-01: Qual a relação entre a popularidade dos repositórios e as suas características de qualidade?**

---

**RQ-02: Qual a relação entre a maturidade do repositórios e as suas características de qualidade ?**

---

**RQ-03: Qual a relação entre a atividade dos repositórios e as suas características de qualidade?**

---

**RQ-04: Qual a relação entre o tamanho dos repositórios e as suas características de qualidade?**
