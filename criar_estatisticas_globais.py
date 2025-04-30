import pandas as pd
import numpy as np


def  agrupar_valores(caminho_arquivo):
    """
    Lê um arquivo Excel, agrupa todos os valores de todas as colunas em um único DataFrame usando flatten.

    Parâmetros:
    caminho_arquivo (str): Caminho do arquivo Excel.

    Retorna:
    pd.DataFrame: DataFrame com todos os valores agrupados.
    """
    # Ler todas as abas do arquivo Excel
    df = pd.read_excel(caminho_arquivo)

    df = df.iloc[:, 1:]  # Remover a primeira coluna
    # Concatenar todas as abas em um único DataFrame
    ##df_consolidado = pd.concat(df.values(), ignore_index=True)

    # Flatten: Agrupar todos os valores em uma única coluna
    valores_agrupados = pd.DataFrame(df.to_numpy().flatten(), columns=['palavras'])

    # Remover valores NaN
    valores_agrupados = valores_agrupados.dropna()

    # Converter para numérico (caso necessário)
    valores_agrupados['palavras'] = pd.to_numeric(valores_agrupados['palavras'], errors='coerce')

    # Remover novamente valores NaN após a conversão
    valores_agrupados = valores_agrupados.dropna()

    return valores_agrupados


def criar_estatisticas_globais(valores_agrupados):

    
    estatisticas_globais = {
        'Média': valores_agrupados['palavras'].mean(),
        'Mediana': valores_agrupados['palavras'].median(),
        'Desvio Padrão': valores_agrupados['palavras'].std(),
        'Máximo': valores_agrupados['palavras'].max(),
        'Mínimo': valores_agrupados['palavras'].min(),
        'Contagem': valores_agrupados['palavras'].count(),
        'Soma': valores_agrupados['palavras'].sum(),
    }

    estatisticas_globais_df = pd.DataFrame([estatisticas_globais])
    
    return estatisticas_globais_df
    

if __name__ == "__main__":
    caminho_arquivo = "C:/Users/Gabriel/Desktop/Artigo_atualizado/tabelas/palavras_por_canal.xlsx"
    
    try:
        # Chamar a função para processar o arquivo
        agrupado = agrupar_valores(caminho_arquivo)
        resultado = criar_estatisticas_globais(agrupado)
        print(resultado)
        resultado.to_excel("C:/Users/Gabriel/Desktop/Artigo_atualizado/tabelas/estatisticas_globais.xlsx", index=False)
        print("Arquivo de estatísticas globais criado com sucesso!")
    
    except Exception as e:
        print(f"Erro ao processar o arquivo: {e}")    
        
     