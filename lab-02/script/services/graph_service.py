import os

import matplotlib.pyplot as plt
import pandas as pd

from script.constants.constants import RESULTS_DIR, SUMMARY_CK_FILE

csv_file_path = os.path.join(RESULTS_DIR, SUMMARY_CK_FILE)
# df = pd.read_csv(csv_file_path)


def generate_graphs():
    # RQ 01 - Qual a relação entre a popularidade dos repositórios e as suas características de qualidade?
    indep_pop = "stargazer_count"
    plot_graphs(df, indep_pop, "cbo_average", indep_pop, "CBO vs Estrelas do projeto")
    plot_graphs(df, indep_pop, "dit_average", indep_pop, "DIT vs Estrelas do projeto")
    plot_graphs(df, indep_pop, "lcom_average", indep_pop, "LCOM vs Estrelas do projeto")

    # # RQ 02 - Qual a relação entre a maturidade dos repositórios e as suas características de qualidade?
    df["Idade (anos)"] = (pd.to_datetime(df["updated_at"]) - pd.to_datetime(df["created_at"])).dt.days / 365.0
    indep_mat = "Idade (anos)"
    plot_graphs(df, indep_mat, "cbo_average", indep_mat, "CBO vs Maturidade do projeto")
    plot_graphs(df, indep_mat, "dit_average", indep_mat, "DIT vs Maturidade do projeto")
    plot_graphs(df, indep_mat, "lcom_average", indep_mat, "LCOM vs Maturidade do projeto")

    # # RQ 03 - Qual a relação entre a atividade dos repositórios e as suas características de qualidade?
    indep_ati = "release_count"
    plot_graphs(df, indep_ati, "cbo_average", indep_ati, "CBO vs Atividade do projeto")
    plot_graphs(df, indep_ati, "dit_average", indep_ati, "DIT vs Atividade do projeto")
    plot_graphs(df, indep_ati, "lcom_average", indep_ati, "LCOM vs Atividade do projeto")

    # RQ 04 - Qual a relação entre o tamanho dos repositórios e as suas características de qualidade?
    indep_tam = "loc_average"
    plot_graphs(df, indep_tam, "cbo_average", indep_tam, "CBO vs Tamanho do projeto")
    plot_graphs(df, indep_tam, "dit_average", indep_tam, "DIT vs Tamanho do projeto")
    plot_graphs(df, indep_tam, "lcom_average", indep_tam, "LCOM vs Tamanho do projeto")

    plt.show()


def plot_graphs(df, independent_var, metric, xlabel, title):
    x = pd.to_numeric(df[independent_var], errors='coerce')
    y = pd.to_numeric(df[metric], errors='coerce')

    plt.figure(figsize=(8, 6))
    plt.scatter(x, y, label=metric, marker='o', color='b')

    plt.xlabel(xlabel)
    plt.ylabel(metric)
    plt.title(title)
    plt.legend()
    plt.grid(True)
