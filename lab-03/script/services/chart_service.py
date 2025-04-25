import os

import matplotlib.pyplot as plt
import pandas as pd
from scipy.stats import spearmanr

from script.constants.constants import RESULTS_DIR, PULL_REQUESTS_FILE

df = pd.read_csv(os.path.join(RESULTS_DIR, PULL_REQUESTS_FILE))
df["feedback_final"] = df["merged"].astype(int)
df["tempo_analise"] = (pd.to_datetime(df["closedAt"]) - pd.to_datetime(df["createdAt"])) / pd.Timedelta(hours=1)
df["descricao_tamanho"] = df["bodyText"].fillna("").apply(len)
df["interacoes"] = df["participants.totalCount"] + df["comments.totalCount"]
df["tamanho_pr"] = df["additions"] + df["deletions"]
df["numero_revisoes"] = df["comments.totalCount"]

RQS = [
    {"id": "RQ01", "x": "tamanho_pr", "y": "feedback_final", "title": "Tamanho do PR vs Feedback Final"},
    {"id": "RQ02", "x": "tempo_analise", "y": "feedback_final", "title": "Tempo de Análise vs Feedback Final"},
    {"id": "RQ03", "x": "descricao_tamanho", "y": "feedback_final", "title": "Tamanho da Descrição vs Feedback Final"},
    {"id": "RQ04", "x": "interacoes", "y": "feedback_final", "title": "Interações no PR vs Feedback Final"},
    {"id": "RQ05", "x": "tamanho_pr", "y": "numero_revisoes", "title": "Tamanho do PR vs Nº de Revisões"},
    {"id": "RQ06", "x": "tempo_analise", "y": "numero_revisoes", "title": "Tempo de Análise vs Nº de Revisões"},
    {"id": "RQ07", "x": "descricao_tamanho", "y": "numero_revisoes", "title": "Tamanho da Descrição vs Nº de Revisões"},
    {"id": "RQ08", "x": "interacoes", "y": "numero_revisoes", "title": "Interações no PR vs Nº de Revisões"}
]


def compute_spearmanr(df, var_x, var_y):
    x = pd.to_numeric(df[var_x], errors='coerce')
    y = pd.to_numeric(df[var_y], errors='coerce')
    mask = x.notna() & y.notna()
    x, y = x[mask], y[mask]
    corr, pval = spearmanr(x, y)
    return corr, pval


def categorize_effect_size(r):
    ar = abs(r)
    if ar < 0.1:
        return 'Muito pequeno'
    elif ar < 0.3:
        return 'Pequeno'
    elif ar < 0.5:
        return 'Moderado'
    else:
        return 'Grande'


def generate_results_table(results):
    headers = ['RQ', 'Descrição', 'Coeficiente', 'p-valor', 'Categoria']
    table = [[str(row[h]) for h in headers] for row in results]
    table.insert(0, headers)
    col_widths = [max(len(str(item)) for item in col) for col in zip(*table)]
    for row in table:
        line = "  ".join(item.ljust(width) for item, width in zip(row, col_widths))
        print(line)


def generate_chart():
    results = []
    for rq in RQS:
        corr, pval = compute_spearmanr(df, rq['x'], rq['y'])
        results.append({
            'RQ': rq['id'],
            'Descrição': rq['title'],
            'Coeficiente': round(corr, 3),
            'p-valor': round(pval, 3),
            'Categoria': categorize_effect_size(corr)
        })

    df_results = pd.DataFrame(results)
    print("Correlação de Pearson para todos os RQs:")
    generate_results_table(results)

    for i, rq in enumerate(RQS):
        x = df[rq['x']]
        y = df[rq['y']]
        med_x = x.median()
        med_y = y.median()

        plt.figure(figsize=(8, 5))
        plt.scatter(x, y, alpha=0.6)
        # cálculo de mediana
        plt.axvline(med_x, linestyle='--', color=f'C{2*i}', label=f'Mediana {rq["x"]}')
        plt.axhline(med_y, linestyle='--', color=f'C{2*i+1}', label=f'Mediana {rq["y"]}')
        plt.title(f"{rq['id']} - {rq['title']}")
        plt.xlabel(rq['x'])
        plt.ylabel(rq['y'])
        plt.legend()
        plt.grid(True)
    plt.show()
