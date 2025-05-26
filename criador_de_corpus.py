import pandas as pd
import numpy as np

def agrupar_valores(caminho_arquivo):
    """
    Lê um arquivo Excel, remove a primeira coluna e agrupa todos os valores de todas as colunas restantes
    em um único DataFrame usando flatten.

    Parâmetros:
    caminho_arquivo (str): Caminho do arquivo Excel.

    Retorna:
    pd.DataFrame: DataFrame com todos os valores agrupados.
    """
    # Ler o arquivo Excel
    df = pd.read_excel(caminho_arquivo)

    # Remover a primeira coluna
    df = df.iloc[:, 1:]

    # Flatten: Agrupar todos os valores em uma única coluna
    valores_agrupados = pd.DataFrame(df.to_numpy().flatten(), columns=['valores'])

    # Remover valores NaN
    valores_agrupados = valores_agrupados.dropna()

    # Verificar se os valores são numéricos e manter apenas os numéricos
    valores_agrupados['valores'] = pd.to_numeric(valores_agrupados['valores'], errors='coerce')

    # Remover novamente valores NaN após a conversão
    valores_agrupados = valores_agrupados.dropna()

    # Resetar o índice para evitar problemas com índices antigos
    valores_agrupados.reset_index(drop=True, inplace=True)

    return valores_agrupados

def amostrar_valores(df, limite_inferior, limite_superior):
    """
    Filtra os valores entre limite_inferior e limite_superior e realiza uma amostragem.

    Parâmetros:
    df (pd.DataFrame): DataFrame com os valores agrupados.
    limite_inferior (float): Limite inferior para o filtro.
    limite_superior (float): Limite superior para o filtro.

    Retorna:
    pd.DataFrame: DataFrame com os valores amostrados.
    """
    # Filtrar os valores entre os limites
    df_filtrado = df[(df['valores'] >= limite_inferior) & (df['valores'] <= limite_superior)]

    # Selecionar 10% dos dados como amostra
    ##df_amostrado = df_filtrado.sample(frac=0.1, random_state=42)

    return df_filtrado

if __name__ == "__main__":
    # Receber o caminho do arquivo como entrada
    caminho_arquivo = "C:/Users/Gabriel/Desktop/Artigo_atualizado/tabelas/palavras_por_canal.xlsx"

    # Agrupar todos os valores em um único DataFrame
    valores_agrupados = agrupar_valores(caminho_arquivo)
    print("Valores agrupados:")
    print(valores_agrupados)

    # Filtrar e amostrar os valores entre (355///355*1.2) pode ser feito apenas pela media
    valores_amostrados = amostrar_valores(valores_agrupados, 364 ,  364*1.2)
    print("\nValores amostrados entre 1000 e 5000:")
    print(valores_amostrados)

    print(valores_agrupados.describe())
    print(valores_amostrados.describe())

  ##  valores_amostrados.to_excel("C:/Users/Gabriel/Desktop/Artigo_atualizado/tabelas/CCCCC.xlsx", index=0)
   ## valores_agrupados.to_excel("C:/Users/Gabriel/Desktop/Artigo_atualizado/tabelas/agrupado.xlsx", index=0)
    # Salvar os resultados em arquivos Excel
    ##valores_amostrados.to_excel("valores_amostrados.xlsx", index=False)
    ##print("\nArquivos 'valores_agrupados.xlsx' e 'valores_amostrados.xlsx' foram salvos com sucesso.")