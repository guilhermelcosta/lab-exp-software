import os
from datetime import datetime

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy.stats as stats
import seaborn as sns

sns.set(style="whitegrid")
plt.rcParams['figure.figsize'] = (10, 6)
RESULTS_FILE = "../data/results.csv"
REPORT_DIR = "../reports"
os.makedirs(REPORT_DIR, exist_ok=True)

df = pd.read_csv(RESULTS_FILE)


def descriptive_analysis(df):
    """
    Gera análise descritiva dos dados e salva em formato Markdown
    """
    # Tempo de resposta
    time_stats = df.groupby(['api', 'complexity'])['time_ms'].describe()

    # Tamanho da resposta
    size_stats = df.groupby(['api', 'complexity'])['size_bytes'].describe()

    # Salvar em formato Markdown
    with open(f"{REPORT_DIR}/statistical_report.md", "w") as f:
        f.write("# Relatório de Análise Estatística\n\n")

        f.write("## Estatísticas Descritivas - Tempo de Resposta (ms)\n\n")
        f.write(time_stats.to_markdown() + "\n\n")

        f.write("## Estatísticas Descritivas - Tamanho da Resposta (bytes)\n\n")
        f.write(size_stats.to_markdown() + "\n\n")

    return time_stats, size_stats


# Versão alternativa com formatação melhorada
def descriptive_analysis_formatted(df):
    """
    Versão com formatação mais detalhada das tabelas
    """
    # Tempo de resposta
    time_stats = df.groupby(['api', 'complexity'])['time_ms'].describe()

    # Tamanho da resposta
    size_stats = df.groupby(['api', 'complexity'])['size_bytes'].describe()

    with open(f"{REPORT_DIR}/statistical_report.md", "w") as f:
        f.write("# Relatório de Análise Estatística\n\n")

        f.write("## Estatísticas Descritivas - Tempo de Resposta (ms)\n\n")
        # Arredonda valores para 2 casas decimais para melhor apresentação
        f.write(time_stats.round(2).to_markdown() + "\n\n")

        f.write("## Estatísticas Descritivas - Tamanho da Resposta (bytes)\n\n")
        f.write(size_stats.round(2).to_markdown() + "\n\n")

        # Adiciona interpretação básica
        f.write("## Observações\n\n")
        f.write("- **GraphQL**: Apresenta tempos de resposta consistentemente maiores que REST\n")
        f.write("- **REST**: Mostra menor variabilidade nos tempos de resposta\n")
        f.write("- **Tamanho das respostas**: Fixo para cada combinação API/complexidade\n")

    return time_stats, size_stats


def hypothesis_testing(df):
    results = []
    complexities = ['simple', 'medium', 'complex']

    for comp in complexities:
        # Filtrar dados
        rest_time = df[(df['api'] == 'REST') & (df['complexity'] == comp)]['time_ms']
        gql_time = df[(df['api'] == 'GraphQL') & (df['complexity'] == comp)]['time_ms']

        rest_size = df[(df['api'] == 'REST') & (df['complexity'] == comp)]['size_bytes']
        gql_size = df[(df['api'] == 'GraphQL') & (df['complexity'] == comp)]['size_bytes']

        # Teste de normalidade (Shapiro-Wilk)
        _, rest_time_norm = stats.shapiro(rest_time)
        _, gql_time_norm = stats.shapiro(gql_time)
        _, rest_size_norm = stats.shapiro(rest_size)
        _, gql_size_norm = stats.shapiro(gql_size)

        # Teste de hipóteses para tempo (RQ1)
        if rest_time_norm > 0.05 and gql_time_norm > 0.05:
            # Dados normais: teste t
            _, time_p = stats.ttest_ind(rest_time, gql_time)
            time_test = "t-test"
        else:
            # Dados não normais: Mann-Whitney
            _, time_p = stats.mannwhitneyu(rest_time, gql_time)
            time_test = "Mann-Whitney"

        # Teste de hipóteses para tamanho (RQ2)
        if rest_size_norm > 0.05 and gql_size_norm > 0.05:
            _, size_p = stats.ttest_ind(rest_size, gql_size)
            size_test = "t-test"
        else:
            _, size_p = stats.mannwhitneyu(rest_size, gql_size)
            size_test = "Mann-Whitney"

        results.append({
            'complexity': comp,
            'time_p_value': time_p,
            'time_test': time_test,
            'size_p_value': size_p,
            'size_test': size_test
        })

    results_df = pd.DataFrame(results)

    with open(f"{REPORT_DIR}/hypothesis_tests.md", "w") as f:
        f.write("# Testes de Hipóteses\n\n")
        f.write("**Nível de significância:** α = 0.05\n\n")
        f.write("## Resultados dos Testes Estatísticos\n\n")
        f.write(results_df.round(4).to_markdown(index=False) + "\n\n")

        f.write("## Interpretação dos Resultados\n\n")
        f.write("| Complexidade | Tempo de Resposta | Tamanho da Resposta |\n")
        f.write("|--------------|-------------------|---------------------|\n")

        for _, row in results_df.iterrows():
            time_result = "Rejeita H0" if row['time_p_value'] < 0.05 else "Não rejeita H0"
            size_result = "Rejeita H0" if row['size_p_value'] < 0.05 else "Não rejeita H0"
            f.write(
                f"| {row['complexity'].title()} | {time_result} (p={row['time_p_value']:.4f}) | {size_result} (p={row['size_p_value']:.4f}) |\n")

        f.write("\n**Legenda:**\n")
        f.write("- **H0:** Não há diferença significativa entre GraphQL e REST\n")
        f.write("- **H1:** Há diferença significativa entre GraphQL e REST\n")
        f.write("- **Rejeita H0:** Diferença estatisticamente significativa (p < 0.05)\n")
        f.write("- **Não rejeita H0:** Diferença não significativa (p ≥ 0.05)\n")

    return results_df


def visualize_results(df):
    # Tempo de resposta
    plt.figure()
    sns.boxplot(x='complexity', y='time_ms', hue='api', data=df)
    plt.title('Tempo de Resposta por Complexidade e Tipo de API')
    plt.ylabel('Tempo (ms)')
    plt.xlabel('Complexidade da Consulta')
    plt.savefig(f"{REPORT_DIR}/response_time.png", bbox_inches='tight')
    plt.close()

    # Tamanho da resposta
    plt.figure()
    sns.boxplot(x='complexity', y='size_bytes', hue='api', data=df)
    plt.title('Tamanho da Resposta por Complexidade e Tipo de API')
    plt.ylabel('Tamanho (bytes)')
    plt.xlabel('Complexidade da Consulta')
    plt.savefig(f"{REPORT_DIR}/response_size.png", bbox_inches='tight')
    plt.close()

    # Comparação de médias
    fig, ax = plt.subplots(1, 2, figsize=(15, 6))

    # Tempo
    time_means = df.groupby(['api', 'complexity'])['time_ms'].mean().unstack()
    time_means.plot(kind='bar', ax=ax[0])
    ax[0].set_title('Média de Tempo de Resposta')
    ax[0].set_ylabel('Tempo (ms)')
    ax[0].set_xlabel('Tipo de API')

    # Tamanho
    size_means = df.groupby(['api', 'complexity'])['size_bytes'].mean().unstack()
    size_means.plot(kind='bar', ax=ax[1])
    ax[1].set_title('Média de Tamanho de Resposta')
    ax[1].set_ylabel('Tamanho (bytes)')
    ax[1].set_xlabel('Tipo de API')

    plt.tight_layout()
    plt.savefig(f"{REPORT_DIR}/comparison.png", bbox_inches='tight')
    plt.close()


def generate_full_report(time_stats, size_stats, hypothesis_results):
    # Análise dinâmica dos resultados para RQ1 (Tempo)
    time_significant = []
    time_patterns = []

    # Obter médias para determinar qual API é mais rápida quando há diferença significativa
    complexities = ['simple', 'medium', 'complex']
    for i, comp in enumerate(complexities):
        rest_mean = df[(df['api'] == 'REST') & (df['complexity'] == comp)]['time_ms'].mean()
        gql_mean = df[(df['api'] == 'GraphQL') & (df['complexity'] == comp)]['time_ms'].mean()

        if hypothesis_results.iloc[i]['time_p_value'] < 0.05:
            time_significant.append(comp)
            if gql_mean < rest_mean:
                time_patterns.append(
                    f"consultas {comp.replace('simple', 'simples').replace('medium', 'médias').replace('complex', 'complexas')}")

    # Análise dinâmica dos resultados para RQ2 (Tamanho)
    size_significant = []
    size_patterns = []

    for i, comp in enumerate(complexities):
        rest_mean = df[(df['api'] == 'REST') & (df['complexity'] == comp)]['size_bytes'].mean()
        gql_mean = df[(df['api'] == 'GraphQL') & (df['complexity'] == comp)]['size_bytes'].mean()

        if hypothesis_results.iloc[i]['size_p_value'] < 0.05:
            size_significant.append(comp)
            if gql_mean < rest_mean:
                size_patterns.append(
                    f"consultas {comp.replace('simple', 'simples').replace('medium', 'médias').replace('complex', 'complexas')}")

    # Gerar padrões observados dinamicamente
    # Para tempo
    if time_patterns:
        time_pattern_text = f"Em {', '.join(time_patterns)}, GraphQL demonstrou desempenho significativamente melhor que REST"
        if len(time_significant) < 3:
            non_significant = [comp for comp in complexities if comp not in time_significant]
            non_sig_text = ', '.join(
                [comp.replace('simple', 'simples').replace('medium', 'médias').replace('complex', 'complexas') for comp in non_significant])
            time_pattern_text += f", enquanto em consultas {non_sig_text} não houve diferença significativa ou REST foi superior."
        else:
            time_pattern_text += "."
    else:
        # Verificar se GraphQL foi consistentemente mais lento
        slower_patterns = []
        for i, comp in enumerate(complexities):
            if hypothesis_results.iloc[i]['time_p_value'] < 0.05:
                rest_mean = df[(df['api'] == 'REST') & (df['complexity'] == comp)]['time_ms'].mean()
                gql_mean = df[(df['api'] == 'GraphQL') & (df['complexity'] == comp)]['time_ms'].mean()
                if gql_mean > rest_mean:
                    slower_patterns.append(comp.replace('simple', 'simples').replace('medium', 'médias').replace('complex', 'complexas'))

        if slower_patterns:
            time_pattern_text = f"Em consultas {', '.join(slower_patterns)}, GraphQL demonstrou desempenho significativamente menor que REST"
            if len(slower_patterns) < 3:
                time_pattern_text += ", enquanto nas demais não houve diferença significativa."
            else:
                time_pattern_text += "."
        else:
            time_pattern_text = "Não foram observadas diferenças significativas consistentes no tempo de resposta entre as APIs."

    # Para tamanho
    if size_patterns:
        size_pattern_text = f"Em {', '.join(size_patterns)}, GraphQL produziu respostas significativamente menores que REST"
        if len(size_significant) < 3:
            non_significant = [comp for comp in complexities if comp not in size_significant]
            non_sig_text = ', '.join(
                [comp.replace('simple', 'simples').replace('medium', 'médias').replace('complex', 'complexas') for comp in non_significant])
            size_pattern_text += f", enquanto em consultas {non_sig_text} não houve diferença significativa ou REST produziu respostas menores."
        else:
            size_pattern_text += "."
    else:
        # Verificar se GraphQL produziu respostas maiores
        larger_patterns = []
        for i, comp in enumerate(complexities):
            if hypothesis_results.iloc[i]['size_p_value'] < 0.05:
                rest_mean = df[(df['api'] == 'REST') & (df['complexity'] == comp)]['size_bytes'].mean()
                gql_mean = df[(df['api'] == 'GraphQL') & (df['complexity'] == comp)]['size_bytes'].mean()
                if gql_mean > rest_mean:
                    larger_patterns.append(comp.replace('simple', 'simples').replace('medium', 'médias').replace('complex', 'complexas'))

        if larger_patterns:
            size_pattern_text = f"Em consultas {', '.join(larger_patterns)}, GraphQL produziu respostas significativamente maiores que REST"
            if len(larger_patterns) < 3:
                size_pattern_text += ", enquanto nas demais não houve diferença significativa."
            else:
                size_pattern_text += "."
        else:
            size_pattern_text = "Não foram observadas diferenças significativas consistentes no tamanho das respostas entre as APIs."

    # Gerar conclusões dinâmicas
    # RQ1 Conclusão
    if time_patterns:
        rq1_conclusion = f"GraphQL demonstrou ser mais rápido que REST em {', '.join(time_patterns)}"
        if len(time_patterns) < 3:
            rq1_conclusion += ", porém equivalente ou inferior nas demais complexidades"
    else:
        if any(hypothesis_results['time_p_value'] < 0.05):
            rq1_conclusion = "GraphQL demonstrou ser mais lento que REST na maioria dos cenários testados"
        else:
            rq1_conclusion = "GraphQL demonstrou desempenho equivalente ao REST em todas as complexidades"

    # RQ2 Conclusão
    if size_patterns:
        rq2_conclusion = f"GraphQL produziu respostas menores que REST em {', '.join(size_patterns)}"
        if len(size_patterns) < 3:
            rq2_conclusion += ", mas equivalente ou maior nas demais complexidades"
    else:
        if any(hypothesis_results['size_p_value'] < 0.05):
            rq2_conclusion = "GraphQL produziu respostas maiores que REST na maioria dos cenários testados"
        else:
            rq2_conclusion = "GraphQL produziu respostas de tamanho equivalente ao REST em todas as complexidades"

    # Recomendações dinâmicas
    if time_patterns and size_patterns:
        recommendation1 = f"Para aplicações com {', '.join(set(time_patterns + size_patterns))}, GraphQL oferece vantagens tanto em velocidade quanto em tamanho de resposta"
        recommendation2 = "Para outros cenários, REST pode ser mais adequado devido ao menor overhead de implementação"
    elif size_patterns:
        recommendation1 = f"Para aplicações com {', '.join(size_patterns)} e necessidade de otimização de banda, GraphQL oferece vantagens em tamanho de resposta"
        recommendation2 = "Para cenários com prioridade na velocidade de resposta, REST pode ser mais adequado"
    elif time_patterns:
        recommendation1 = f"Para aplicações com {', '.join(time_patterns)} e necessidade de velocidade, GraphQL oferece vantagens em tempo de resposta"
        recommendation2 = "Para outros cenários, REST pode ser mais adequado devido à sua simplicidade"
    else:
        recommendation1 = "Para a maioria dos cenários testados, REST demonstrou desempenho superior ou equivalente"
        recommendation2 = "GraphQL pode ser considerado quando há necessidade específica de flexibilidade na consulta de dados"

    report = f"""
# RELATÓRIO FINAL: COMPARAÇÃO GRAPHQL VS REST

**Data de execução:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
**Total de medições:** {len(df)}
**Ambiente experimental:** 
- Processador: Ryzen 5 3600
- RAM: 16GB DDR4
- SO: Windows 11 (WSL)
- Python 3.12.3
- Bibliotecas: Flask 2.2.2, Flask-GraphQL 2.0.1, graphene 3.2, requests 2.28.1

## 1. Introdução
Este relatório apresenta os resultados de um experimento controlado comparando APIs GraphQL e REST. As perguntas de pesquisa são:

**RQ1:** Respostas às consultas GraphQL são mais rápidas que respostas às consultas REST?

**RQ2:** Respostas às consultas GraphQL têm tamanho menor que respostas às consultas REST?

Hipóteses:
- H0 (RQ1): Não há diferença significativa no tempo de resposta
- H1 (RQ1): GraphQL é mais rápido que REST
- H0 (RQ2): Não há diferença significativa no tamanho das respostas
- H1 (RQ2): GraphQL produz respostas menores que REST

## 2. Metodologia

### 2.1. Desenho Experimental
- **Variáveis independentes:** Tipo de API (REST, GraphQL), Complexidade (simples, média, complexa)
- **Variáveis dependentes:** Tempo de resposta (ms), Tamanho da resposta (bytes)
- **Tratamentos:** 6 combinações (2 APIs × 3 complexidades)
- **Repetições:** 30 execuções por tratamento (total 180 medições)
- **Ambiente:** Local (localhost), sem tráfego de rede externa

### 2.2. Execução
1. Banco de dados inicializado com dados de exemplo
2. APIs REST e GraphQL iniciadas em portas diferentes
3. Script de benchmark executado sequencialmente:
   - 30 requisições para cada combinação
   - Tempo medido do início da requisição até resposta completa
   - Tamanho medido pelo conteúdo da resposta

### 2.3. Análise Estatística
- Teste de normalidade (Shapiro-Wilk)
- Testes paramétricos (t-test) ou não-paramétricos (Mann-Whitney) conforme distribuição
- Nível de significância: α = 0.05

## 3. Resultados

### 3.1. Estatísticas Descritivas

**Tempo de Resposta (ms):**

{time_stats.round(4).to_markdown()}

**Tamanho da Resposta (bytes):**

{size_stats.round(2).to_markdown()}

### 3.2. Testes de Hipóteses

{hypothesis_results.round(4).to_markdown(index=False)}

### 3.3. Visualizações
![Tempo de Resposta](response_time.png)
![Tamanho da Resposta](response_size.png)
![Comparação de Médias](comparison.png)

## 4. Análise e Discussão

### RQ1: Tempo de Resposta
- Consultas simples: {'Rejeita H0' if hypothesis_results.iloc[0]['time_p_value'] < 0.05 else 'Não rejeita H0'} (p = {hypothesis_results.iloc[0]['time_p_value']:.4f})
- Consultas médias: {'Rejeita H0' if hypothesis_results.iloc[1]['time_p_value'] < 0.05 else 'Não rejeita H0'} (p = {hypothesis_results.iloc[1]['time_p_value']:.4f})
- Consultas complexas: {'Rejeita H0' if hypothesis_results.iloc[2]['time_p_value'] < 0.05 else 'Não rejeita H0'} (p = {hypothesis_results.iloc[2]['time_p_value']:.4f})

Padrão observado: {time_pattern_text}

### RQ2: Tamanho da Resposta
- Consultas simples: {'Rejeita H0' if hypothesis_results.iloc[0]['size_p_value'] < 0.05 else 'Não rejeita H0'} (p = {hypothesis_results.iloc[0]['size_p_value']:.4f})
- Consultas médias: {'Rejeita H0' if hypothesis_results.iloc[1]['size_p_value'] < 0.05 else 'Não rejeita H0'} (p = {hypothesis_results.iloc[1]['size_p_value']:.4f})
- Consultas complexas: {'Rejeita H0' if hypothesis_results.iloc[2]['size_p_value'] < 0.05 else 'Não rejeita H0'} (p = {hypothesis_results.iloc[2]['size_p_value']:.4f})

Padrão observado: {size_pattern_text}

### 4.1. Ameaças à Validade
1. **Validade interna:** Variações no ambiente de execução foram minimizadas executando em máquina dedicada
2. **Validade externa:** Resultados específicos para modelo de dados de blog - outros domínios podem variar
3. **Viés de implementação:** Mesma base de dados e lógica de negócio usada em ambas APIs

## 5. Conclusões
- **RQ1:** {rq1_conclusion}.
- **RQ2:** {rq2_conclusion}.

Recomendações:
- {recommendation1}.
- {recommendation2}.

Limitações e trabalhos futuros:
- Testar com diferentes estruturas de dados
- Avaliar impacto em redes de baixa largura de banda
- Medir consumo de recursos no servidor
"""

    with open(f"{REPORT_DIR}/final_report.md", "w", encoding="utf-8") as f:
        f.write(report)


if __name__ == "__main__":
    print("Iniciando análise dos resultados...")
    time_stats, size_stats = descriptive_analysis(df)
    hypothesis_results = hypothesis_testing(df)
    visualize_results(df)
    generate_full_report(time_stats, size_stats, hypothesis_results)
    print("Análise concluída! Relatórios salvos em:", REPORT_DIR)
