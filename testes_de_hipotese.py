import numpy as np
from scipy.stats import mannwhitneyu, shapiro, anderson
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def teste_shapiro_wilk(dados):
    estatistica, p_valor = shapiro(dados)
    return estatistica, p_valor


def teste_anderson_darling(dados):
    resultado = anderson(dados)
    return resultado.statistic, resultado.critical_values


def teste_mann_whitney_u(grupo1, grupo2):
    estatistica_u, p_valor = mannwhitneyu(grupo1, grupo2)
    return estatistica_u, p_valor


def plotar_distribuicao(dados, titulo="Distribuição da População"):
    """
    Plota o histograma com a curva de densidade para os dados fornecidos.
    """
    plt.figure(figsize=(10, 6))
    sns.histplot(dados, kde=True, bins=30, color='blue', alpha=0.7)
    plt.title(titulo, fontsize=16)
    plt.xlabel('Valores', fontsize=14)
    plt.ylabel('Frequência', fontsize=14)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.show()


if __name__ == "__main__":
    caminho_arquivo = "C:/Users/Gabriel/Desktop/Artigo_atualizado/tabelas/agrupado.xlsx"  # Substitua pelo caminho do seu arquivo Excel
    
    # Ler o arquivo Excel
    df = pd.read_excel(caminho_arquivo)
    df = df.apply(pd.to_numeric, errors='coerce')  # Converte todas as colunas para numérico
    df = df.dropna()  # Remover linhas com valores ausentes
    df = df.reset_index(drop=True)  # Reiniciar o índice após a remoção de linhas

    df_amostra = df[(df['valores'] >= 300*0.8) & (df['valores'] <= 300*1.2)]
    df_amostra = df_amostra.dropna()  # Remover linhas com valores ausentes na amostra
    df_amostra = df_amostra.reset_index(drop=True)  # Reiniciar o índice após a remoção de linhas

    # Substitua 'coluna_grupo1' e 'coluna_grupo2' pelos nomes das colunas no seu arquivo
    grupo1 = df['valores']

    # Teste de normalidade para o grupo 1
    estatistica_shapiro1, p_valor_shapiro1 = teste_shapiro_wilk(grupo1)
    estatistica_anderson1, valores_criticos1 = teste_anderson_darling(grupo1)

    estatistica_shapiro2, p_valor_shapiro2 = teste_shapiro_wilk(df_amostra['valores'])
    estatistica_anderson2, valores_criticos2 = teste_anderson_darling(df_amostra['valores'])

    # Definir o nível de significância
    nivel_significancia = 0.05

    print(df_amostra.describe()) 
    print(df_amostra['valores'])

    print("Grupo 1 - Shapiro-Wilk: Estatística =", estatistica_shapiro1, ", p-valor =", p_valor_shapiro1)
    print("Grupo 1 - Anderson-Darling: Estatística =", estatistica_anderson1, ", Valores críticos =", valores_criticos1)
    print("teste para corpus amostrado = ", estatistica_shapiro2, ", p-valor =", p_valor_shapiro2)
    print("teste para corpus amostrado = ", estatistica_anderson2, ", Valores críticos =", valores_criticos2)

    # Teste Shapiro-Wilk
    if p_valor_shapiro1 < nivel_significancia:
        print("Grupo 1 - Os dados NÃO seguem uma distribuição normal (Rejeita H0) para Shapiro-wilki.")
    else:
        print("Grupo 1 - Os dados seguem uma distribuição normal (Não rejeita H0) para Shapiro-wilki.")

    if p_valor_shapiro2 < nivel_significancia:
        print("Grupo amostrado - Os dados NÃO seguem uma distribuição normal (Rejeita H0) para Shapiro-wilki.")
    else:   
        print("Grupo amostrado - Os dados seguem uma distribuição normal (Não rejeita H0) para Shapiro-wilki.")

    # Teste Anderson-Darling
    nivel_significancia_ad = 5  # Escolha o nível de significância em %
    indice_critico = [15, 10, 5, 2.5, 1].index(nivel_significancia_ad)
    valor_critico = valores_criticos1[indice_critico]

    if estatistica_anderson1 > valor_critico:
        print(f"Grupo 1 - Os dados NÃO seguem uma distribuição normal (Rejeita H0 para {nivel_significancia_ad}%) para Anderson-Darling.")
    else:
        print(f"Grupo 1 - Os dados seguem uma distribuição normal (Não rejeita H0 para {nivel_significancia_ad}%) para Anderson-Darling.")

    # Plotar a distribuição da população
    plotar_distribuicao(grupo1, titulo="Distribuição da População - Grupo 1")
    plotar_distribuicao(df_amostra['valores'], titulo="Distribuição da População - Amostra")