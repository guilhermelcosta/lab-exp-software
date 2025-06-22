# 🔍 GraphQL vs REST – Comparação de Desempenho

Este repositório contém um experimento controlado comparando o desempenho entre APIs GraphQL e REST, com foco em **tempo de resposta** e **tamanho das respostas**.

## 📑 Sobre o Relatório

O relatório completo está disponível em [`relatorio_final.md`](./relatorio_final.md), com análises estatísticas, gráficos e discussões detalhadas.

### Objetivos da Pesquisa

- **RQ1:** GraphQL responde mais rápido que REST?
- **RQ2:** GraphQL retorna respostas menores que REST?

Foram formuladas hipóteses nulas e alternativas para ambas as perguntas, e os resultados foram avaliados com testes estatísticos apropriados.

## 🧪 Metodologia

- **Total de medições:** 180 (30 por cenário)
- **Tipos de consulta:** simples, média, complexa
- **Ambiente:** localhost via WSL
- **Ferramentas principais:**  
  - `Flask`, `Flask-GraphQL`, `graphene`, `requests`  
  - Python 3.12.3

## 📊 Principais Resultados

- **GraphQL foi mais lento** que REST em todos os cenários
- **GraphQL produziu respostas maiores** que REST
- Diferenças estatisticamente significativas (p < 0.05) em todos os testes

Veja os gráficos no relatório para detalhes visuais:
- `response_time.png`
- `response_size.png`
- `comparison.png`

## 💡 Conclusões

- REST teve desempenho superior ou equivalente à GraphQL nas métricas avaliadas
- GraphQL é mais indicado quando há necessidade de **flexibilidade na consulta**

## 📁 Estrutura do Projeto

```bash
.
├── relatorio_final.md         # Relatório completo do experimento
├── response_time.png          # Gráfico do tempo de resposta
├── response_size.png          # Gráfico do tamanho das respostas
├── comparison.png             # Comparação de médias
├── graphql_api/               # Implementação da API GraphQL
├── rest_api/                  # Implementação da API REST
├── benchmark.py               # Script de benchmark (requisições e medições)
└── requirements.txt           # Bibliotecas necessárias
````

## 🚀 Como Executar

1. Clone o repositório:

   ```bash
   git clone https://github.com/seu-usuario/graphql-vs-rest.git
   cd graphql-vs-rest
   ```

2. Crie um ambiente virtual e instale as dependências:

   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. Execute as APIs em terminais separados:

   ```bash
   python graphql_api/app.py
   python rest_api/app.py
   ```

4. Rode o benchmark:

   ```bash
   python benchmark.py
   ```
