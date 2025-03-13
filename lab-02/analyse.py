import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Ler os dados do arquivo CSV de resumo
df = pd.read_csv("results/ck_results/ck_summary.csv")

# Exibir as primeiras linhas para verificar os dados
print(df.head())

# Plotando um gráfico de dispersão (scatter plot) entre CBO e DIT
plt.figure(figsize=(10, 6))
sns.scatterplot(data=df, x='cbo', y='dit')
plt.title('Dispersão entre CBO e DIT')
plt.xlabel('CBO (Coupling Between Objects)')
plt.ylabel('DIT (Depth of Inheritance Tree)')
plt.show()

# Gerar um gráfico de barras para visualizar a média de cada métrica
metrics = ['cbo', 'dit', 'lcom']
df[metrics].mean().plot(kind='bar', figsize=(10, 6), color='skyblue')
plt.title('Média das Métricas CK')
plt.ylabel('Valor médio')
plt.show()

# Histograma para visualizar a distribuição de CBO
plt.figure(figsize=(10, 6))
sns.histplot(df['cbo'], kde=True, bins=20, color='salmon')
plt.title('Distribuição de CBO (Coupling Between Objects)')
plt.xlabel('CBO')
plt.ylabel('Frequência')
plt.show()
