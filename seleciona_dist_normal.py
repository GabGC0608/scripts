import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import shapiro, anderson
import os
import shutil

def amostra_bilateral_normal(valores, tamanho_amostra=500):
    # Ordena os valores
    valores_ordenados = np.sort(valores)
    n = len(valores_ordenados)
    # Encontra o índice central
    centro = n // 2
    # Seleciona metade para cada lado do centro
    metade = tamanho_amostra // 2
    if tamanho_amostra % 2 == 0:
        amostra = np.concatenate([
            valores_ordenados[centro - metade:centro],
            valores_ordenados[centro:centro + metade]
        ])
    else:
        amostra = np.concatenate([
            valores_ordenados[centro - metade:centro],
            [valores_ordenados[centro]],
            valores_ordenados[centro + 1:centro + metade + 1]
        ])
    return amostra

def plotar_distribuicao(dados, titulo="Distribuição"):
    plt.figure(figsize=(10, 6))
    sns.histplot(dados, kde=True, bins=30, color='blue', alpha=0.7)
    plt.title(titulo, fontsize=16)
    plt.xlabel('Valores', fontsize=14)
    plt.ylabel('Frequência', fontsize=14)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.show()

def teste_shapiro_anderson(dados, nome="Grupo"):
    estatistica_shapiro, p_shapiro = shapiro(dados)
    resultado_anderson = anderson(dados)
    estatistica_anderson = resultado_anderson.statistic
    valores_criticos = resultado_anderson.critical_values
    print(f"{nome} - Shapiro-Wilk: Estatística = {estatistica_shapiro}, p-valor = {p_shapiro}")
    print(f"{nome} - Anderson-Darling: Estatística = {estatistica_anderson}, Valores críticos = {valores_criticos}")
    nivel_significancia = 0.05
    if p_shapiro < nivel_significancia:
        print(f"{nome} - NÃO segue normalidade (Shapiro-Wilk)")
    else:
        print(f"{nome} - Segue normalidade (Shapiro-Wilk)")
    nivel_significancia_ad = 5  # %
    indice_critico = [15, 10, 5, 2.5, 1].index(nivel_significancia_ad)
    valor_critico = valores_criticos[indice_critico]
    if estatistica_anderson > valor_critico:
        print(f"{nome} - NÃO segue normalidade (Anderson-Darling, {nivel_significancia_ad}%)")
    else:
        print(f"{nome} - Segue normalidade (Anderson-Darling, {nivel_significancia_ad}%)")
    print()

def selecionar_textos_por_n_palavras(amostra_palavras, pasta_textos, pasta_destino):
    if not os.path.exists(pasta_destino):
        os.makedirs(pasta_destino)
    amostra_restante = list(amostra_palavras)
    for nome_arquivo in os.listdir(pasta_textos):
        if nome_arquivo.endswith('.txt'):
            caminho = os.path.join(pasta_textos, nome_arquivo)
            with open(caminho, 'r', encoding='utf-8') as f:
                texto = f.read()
            n_palavras = len(texto.split())
            if n_palavras in amostra_restante:
                shutil.copy2(caminho, os.path.join(pasta_destino, nome_arquivo))
                amostra_restante.remove(n_palavras)
            if not amostra_restante:
                break

if __name__ == "__main__":
    caminho_arquivo = "C:/Users/Gabriel/Desktop/Artigo_atualizado/tabelas/agrupado.xlsx"
    pasta_textos = "C:/Users/Gabriel/Desktop/MEU_ARTIGO/DADOS_CORPUS/corpus_cortado"
    pasta_destino = "C:/Users/Gabriel/Desktop/MEU_ARTIGO/DADOS_CORPUS/testes_selecionados"

    df = pd.read_excel(caminho_arquivo)
    df = df.dropna(subset=['valores'])
    valores = df['valores'].to_numpy()

    print("População completa:")
    plotar_distribuicao(valores, "Distribuição da População Completa")
    teste_shapiro_anderson(valores, nome="População")

    # Seleciona amostra bilateralmente normal
    amostra = amostra_bilateral_normal(valores, tamanho_amostra=500)
    print("Amostra bilateralmente normal:")
    plotar_distribuicao(amostra, "Distribuição da Amostra Bilateralmente Normal")
    teste_shapiro_anderson(amostra, nome="Amostra")

    # Seleciona textos reais com o mesmo número de palavras da amostra
    selecionar_textos_por_n_palavras(amostra, pasta_textos, pasta_destino)
    print(f"Textos selecionados foram copiados para: {pasta_destino}")