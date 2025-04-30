import pandas as pd

def Faz_media_acumulada(caminho_arquivo):
    """
    Calcula a média acumulada para todas as colunas numéricas de um DataFrame
    e retorna um novo DataFrame contendo apenas as médias acumuladas.

    Parâmetros:
    caminho_arquivo (str): Caminho do arquivo Excel.

    Retorna:
    pd.DataFrame: DataFrame com as médias acumuladas para cada coluna.
    """
    # Ler o arquivo Excel
    df = pd.read_excel(caminho_arquivo)

    # Criar um novo DataFrame para armazenar as médias acumuladas
    medias_acumuladas = pd.DataFrame()

    # Calcular a média acumulada para cada coluna numérica
    for coluna in df.select_dtypes(include=['number']).columns:
        medias_acumuladas[coluna + '_Média_Acumulada'] = df[coluna].expanding().mean()

    return medias_acumuladas


if __name__ == "__main__":
    caminho_arquivo = "C:/Users/Gabriel/Desktop/Artigo_atualizado/tabelas/palavras_por_canal.xlsx"
    
    try:
        # Chamar a função para processar o arquivo
        df_medias_acumuladas = Faz_media_acumulada(caminho_arquivo)

        # Exibir o DataFrame com as médias acumuladas
        print(df_medias_acumuladas)

        # Salvar o DataFrame em um arquivo Excel
        df_medias_acumuladas.to_excel("C:/Users/Gabriel/Desktop/Artigo_atualizado/tabelas/medias_acumuladas.xlsx", index=1)
        print("Arquivo com médias acumuladas criado com sucesso!")

    except Exception as e:
        print(f"Erro ao processar o arquivo: {e}")