# Testes de Hipóteses

**Nível de significância:** α = 0.05

## Resultados dos Testes Estatísticos

| complexity   |   time_p_value | time_test    |   size_p_value | size_test   |
|:-------------|---------------:|:-------------|---------------:|:------------|
| simple       |              0 | Mann-Whitney |              0 | t-test      |
| medium       |              0 | Mann-Whitney |              0 | t-test      |
| complex      |              0 | t-test       |              0 | t-test      |

## Interpretação dos Resultados

| Complexidade | Tempo de Resposta | Tamanho da Resposta |
|--------------|-------------------|---------------------|
| Simple | Rejeita H0 (p=0.0000) | Rejeita H0 (p=0.0000) |
| Medium | Rejeita H0 (p=0.0000) | Rejeita H0 (p=0.0000) |
| Complex | Rejeita H0 (p=0.0000) | Rejeita H0 (p=0.0000) |

**Legenda:**
- **H0:** Não há diferença significativa entre GraphQL e REST
- **H1:** Há diferença significativa entre GraphQL e REST
- **Rejeita H0:** Diferença estatisticamente significativa (p < 0.05)
- **Não rejeita H0:** Diferença não significativa (p ≥ 0.05)
