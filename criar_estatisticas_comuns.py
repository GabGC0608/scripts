import pandas as pd
import numpy as np  


def criar_estatisticas_P_coluna(caminho_arquivo):
    """
    Cria um DataFrame com estatísticas (média, mediana, desvio padrão, máximo e mínimo)
    para cada coluna de um DataFrame existente.

    Parâmetros:
    df (pd.DataFrame): DataFrame original.

    Retorna:
    pd.DataFrame: DataFrame com estatísticas como linhas.
    """
    df = pd.read_excel(caminho_arquivo)
    
    estatisticas = {
        'Média': df.mean(),
        'Mediana': df.median(),
        'Desvio Padrão': df.std(),
        'Máximo': df.max(),
        'Mínimo': df.min(),
        'contagem': df.count(),
        'Soma': df.sum(),

    }

    estatisticas_df = pd.DataFrame(estatisticas)
    
    return estatisticas_df.T

if __name__ == "__main__":

    caminho_arquivo = "C:/Users/Gabriel/Desktop/Artigo_atualizado/tabelas/palavras_por_canal.xlsx"
    
    try:
        # Chamar a função para processar o arquivo
        
        
        estatisticas_df = criar_estatisticas_P_coluna(caminho_arquivo)

        print(estatisticas_df)

        estatisticas_df.to_excel("C:/Users/Gabriel/Desktop/Artigo_atualizado/tabelas/estatisticas_por_canal.xlsx", index=False)

    except Exception as e:
        print(f"Erro ao processar o arquivo: {e}") 
        
      