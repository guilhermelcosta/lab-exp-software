import os
import matplotlib.pyplot as plt
import pandas as pd

from script.constants.constants import RESULTS_DIR, PULL_REQUESTS_FILE

df = pd.read_csv(os.path.join(RESULTS_DIR, PULL_REQUESTS_FILE))

# Pré-processamento
df["feedback_final"] = df["merged"].astype(int)  # 1 se foi aceito, 0 se não foi
df["tempo_analise"] = (pd.to_datetime(df["closedAt"]) - pd.to_datetime(df["createdAt"])).dt.total_seconds() / 3600  # em horas
df["descricao_tamanho"] = df["bodyText"].fillna("").apply(len)
df["interacoes"] = df["participants.totalCount"] + df["comments.totalCount"]
df["tamanho_pr"] = df["additions"] + df["deletions"]
df["numero_revisoes"] = df["comments.totalCount"]

# Gráficos
def generate_graphs():
    # RQ01
    plot_graphs(df, "tamanho_pr", "feedback_final", "Tamanho do PR", "Feedback Final", "RQ01 - Tamanho dos PRs vs Feedback Final")

    # RQ02
    plot_graphs(df, "tempo_analise", "feedback_final", "Tempo de Análise (h)", "Feedback Final", "RQ02 - Tempo de Análise vs Feedback Final")

    # RQ03
    plot_graphs(df, "descricao_tamanho", "feedback_final", "Tamanho da Descrição", "Feedback Final", "RQ03 - Descrição dos PRs vs Feedback Final")

    # RQ04
    plot_graphs(df, "interacoes", "feedback_final", "Interações no PR", "Feedback Final", "RQ04 - Interações vs Feedback Final")

    # RQ05
    plot_graphs(df, "tamanho_pr", "numero_revisoes", "Tamanho do PR", "Nº de Revisões", "RQ05 - Tamanho dos PRs vs Nº de Revisões")

    # RQ06
    plot_graphs(df, "tempo_analise", "numero_revisoes", "Tempo de Análise (h)", "Nº de Revisões", "RQ06 - Tempo de Análise vs Nº de Revisões")

    # RQ07
    plot_graphs(df, "descricao_tamanho", "numero_revisoes", "Tamanho da Descrição", "Nº de Revisões", "RQ07 - Descrição dos PRs vs Nº de Revisões")

    # RQ08
    plot_graphs(df, "interacoes", "numero_revisoes", "Interações no PR", "Nº de Revisões", "RQ08 - Interações vs Nº de Revisões")

    plt.show()

def plot_graphs(df, independent_var, metric, xlabel, ylabel, title):
    x = pd.to_numeric(df[independent_var], errors='coerce')
    y = pd.to_numeric(df[metric], errors='coerce')

    plt.figure(figsize=(8, 6))
    plt.scatter(x, y, alpha=0.7)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.grid(True)

if __name__ == "__main__":
    generate_graphs()
