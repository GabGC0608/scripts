import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def extrair_coluna_de_todas_abas(arquivo_excel, coluna_alvo='num_palavras', total_abas=49):
    """
    Extrai uma coluna específica de todas as abas de um arquivo Excel.
    
    Parâmetros:
    arquivo_excel (str): Caminho para o arquivo Excel (.xlsx)
    coluna_alvo (str): Nome da coluna a ser extraída
    total_abas (int): Número de abas a processar
    
    Retorna:
    pd.DataFrame: DataFrame com as colunas de todas as abas
    """
    # Ler todos os nomes de abas do arquivo Excel
    todas_abas = pd.ExcelFile(arquivo_excel).sheet_names
    
    # Verificar se há abas suficientes
    if len(todas_abas) < total_abas:
        raise ValueError(f"O arquivo Excel deve ter pelo menos {total_abas} abas. Encontradas: {len(todas_abas)}")
    
    # Lista para armazenar os DataFrames de cada aba
    dfs = []
    
    # Percorrer as abas
    for aba in todas_abas[:total_abas]:
        try:
            # Ler a aba atual
            df_aba = pd.read_excel(arquivo_excel, sheet_name=aba)
            
            # Verificar se a coluna existe na aba
            if coluna_alvo in df_aba.columns:
                # Criar um DataFrame temporário com a coluna desejada
                temp_df = pd.DataFrame({aba: df_aba[coluna_alvo]})
                dfs.append(temp_df)
                
            else:
                print(f"Aviso: A aba '{aba}' não possui coluna '{coluna_alvo}'.")
                # Criar coluna com valores NA
                temp_df = pd.DataFrame({aba: [pd.NA] * len(df_aba)})
                dfs.append(temp_df)
                
        except Exception as e:
            print(f"Erro ao processar aba '{aba}': {str(e)}")
            # Criar coluna de erro
            temp_df = pd.DataFrame({f"{aba}_erro": [pd.NA] * 100})  # Tamanho padrão
            dfs.append(temp_df)
    
    # Concatenar todos os DataFrames
    df_consolidado = pd.concat(dfs, axis=1)
    
    # Preencher valores ausentes com NaN
    df_consolidado = df_consolidado.fillna(np.nan)
    
    # Garantir que as colunas sejam numéricas
    df_consolidado = df_consolidado.apply(pd.to_numeric, errors='coerce')
    
    return df_consolidado


#plotar palavras por canal
def plotar_palavras_por_canal(df):
    """
    Plota um gráfico de barras para a contagem de palavras por canal.

    Parâmetros:
    df (pd.DataFrame): DataFrame com os dados a serem plotados.
    """
    
    plt.figure(figsize=(20, 18))
    for coluna in df.columns:
        plt.plot(df.index, df[coluna])

    plt.title('Número de Palavras por Aba')
    plt.xlabel('Índice (linhas dos dados)')
    plt.ylabel('Número de Palavras')
    plt.legend(loc='upper right', fontsize='small', ncol=2)
    plt.grid(True)
    plt.tight_layout()
    plt.show()


    


# Exemplo de uso:
if __name__ == "__main__":
    caminho_arquivo = "C:/Users/Gabriel/Desktop/Artigo_atualizado/tabelas/dados_por_canal.xlsx"
    
    try:
        # Chamar a função para processar o arquivo
        resultado = extrair_coluna_de_todas_abas(caminho_arquivo)
        #estatisticas_df = criar_estatisticas_P_coluna(resultado)
        #estatisticas_globais_df = criar_estatisticas_globais(resultado)
        # Plotar o gráfico de palavras por canal
        plotar_palavras_por_canal(resultado)
        
        # Mostrar informações completas do resultado
        """print(f"\nDataFrame consolidado criado com {len(resultado.columns)} colunas (abas).")
        print(f"Total de linhas: {len(resultado)}")
        
        # Exibir todas as linhas
        with pd.option_context('display.max_rows', None, 'display.max_columns', None):
            print("\nDataFrame completo:")
            print(resultado)
        
        # Informações e estatísticas
        print("\nInformações do DataFrame:")
        resultado.info()
        
        print("\nEstatísticas descritivas:")
        print(estatisticas_df)"""
        
        # Salvar o resultado
        ##caminho_saida1 = "C:/Users/Gabriel/Desktop/Artigo_atualizado/tabelas/palavras_por_canalAAA.xlsx"
      
        
    except Exception as e:
        print(f"\nErro ao processar o arquivo: {str(e)}")