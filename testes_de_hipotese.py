import numpy as np
from scipy.stats import mannwhitneyu, shapiro, anderson
import pandas as pd


def teste_shapiro_wilk(dados):
    estatistica, p_valor = shapiro(dados)
    return estatistica, p_valor


def teste_anderson_darling(dados):
    resultado = anderson(dados)
    return resultado.statistic, resultado.critical_values


def teste_mann_whitney_u(grupo1, grupo2):
    estatistica_u, p_valor = mannwhitneyu(grupo1, grupo2)
    return estatistica_u, p_valor


if __name__ == "__main__":
    caminho_arquivo = "C:/Users/Gabriel/Desktop/Artigo_atualizado/tabelas/agrupado.xlsx"  # Substitua pelo caminho do seu arquivo Excel
    
    # Ler o arquivo Excel
    df = pd.read_excel(caminho_arquivo)
    df = df.dropna()  # Remover linhas com valores ausentes

    # Substitua 'coluna_grupo1' e 'coluna_grupo2' pelos nomes das colunas no seu arquivo
    grupo1 = df['valores']
    #grupo2 = df['coluna_grupo2']
    

    # Teste de normalidade para o grupo 1
    estatistica_shapiro1, p_valor_shapiro1 = teste_shapiro_wilk(grupo1)
    estatistica_anderson1, valores_criticos1 = teste_anderson_darling(grupo1)

    # Teste de Mann-Whitney U
    #estatistica_u, p_valor_mann_whitney = teste_mann_whitney_u(grupo1, grupo2)


# Definir o nível de significância
nivel_significancia = 0.05

# Teste Shapiro-Wilk
if p_valor_shapiro1 < nivel_significancia:
    print("Grupo 1 - Os dados NÃO seguem uma distribuição normal (Rejeita H0) para Shapiro-wilki.")
else:
    print("Grupo 1 - Os dados seguem uma distribuição normal (Não rejeita H0) para Shapiro-wilki.")

# Teste Anderson-Darling
nivel_significancia_ad = 5  # Escolha o nível de significância em %
indice_critico = [15, 10, 5, 2.5, 1].index(nivel_significancia_ad)
valor_critico = valores_criticos1[indice_critico]

if estatistica_anderson1 > valor_critico:
    print(f"Grupo 1 - Os dados NÃO seguem uma distribuição normal (Rejeita H0 para {nivel_significancia_ad}%) para Anderson-Darling.")
else:
    print(f"Grupo 1 - Os dados seguem uma distribuição normal (Não rejeita H0 para {nivel_significancia_ad}%) para Anderson-Darling.")

# Resultados
##print("Grupo 1 - Shapiro-Wilk: Estatística =", estatistica_shapiro1, ", p-valor =", p_valor_shapiro1)

##print("Grupo 1 - Anderson-Darling: Estatística =", estatistica_anderson1, ", Valores críticos =", valores_criticos1)
    
    #print("\nGrupo 2 - Shapiro-Wilk: Estatística =", estatistica_shapiro2, ", p-valor =", p_valor_shapiro2)
    ##print("\nTeste de Mann-Whitney U: Estatística U =", estatistica_u, ", p-valor =", p_valor_mann_whitney)
