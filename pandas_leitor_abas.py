import pandas as pd
import numpy as np

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
def criar_estatisticas_globais(df):
    # Estatísticas para todos os valores combinados
   
    todos_valores = df.values.flatten()  # Combina todos os valores em um único array
    todos_valores = todos_valores[~pd.isna(todos_valores)]  # Remove valores NaN
    
    estatisticas_globais = {
        'Média': todos_valores.mean(),
        'Mediana': np.median(todos_valores),
        'Desvio Padrão': todos_valores.std(),
        'Máximo': todos_valores.max(),
        'Mínimo': todos_valores.min(),
        'Contagem': len(todos_valores),
        'Soma': todos_valores.sum(),
    }
    estatisticas_globais_df = pd.DataFrame(estatisticas_globais, index=[0])
    return estatisticas_globais_df

def criar_estatisticas_P_coluna(df):
    """
    Cria um DataFrame com estatísticas (média, mediana, desvio padrão, máximo e mínimo)
    para cada coluna de um DataFrame existente.

    Parâmetros:
    df (pd.DataFrame): DataFrame original.

    Retorna:
    pd.DataFrame: DataFrame com estatísticas como linhas.
    """
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

# Exemplo de uso:
if __name__ == "__main__":
    caminho_arquivo = "C:/Users/Gabriel/Desktop/Artigo_atualizado/tabelas/dados_por_canal.xlsx"
    
    try:
        # Chamar a função para processar o arquivo
        resultado = extrair_coluna_de_todas_abas(caminho_arquivo)
        estatisticas_df = criar_estatisticas_P_coluna(resultado)
        estatisticas_globais_df = criar_estatisticas_globais(resultado)
        
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
        caminho_saida1 = "C:/Users/Gabriel/Desktop/Artigo_atualizado/tabelas/palavras_por_canalAAA.xlsx"
        ##caminho_saida2 = "C:/Users/Gabriel/Desktop/Artigo_atualizado/tabelas/estatisticas_palavras_por_canal.xlsx"
        ##caminho_saida3 = "C:/Users/Gabriel/Desktop/Artigo_atualizado/tabelas/estatisticas_globais_palavras_por_canal.xlsx"
        
        resultado.to_excel(caminho_saida1, index=True)
        estatisticas_df.to_excel(caminho_saida2, index=True)
        estatisticas_globais_df.to_excel(caminho_saida3, index=True)

        print(f"\nDados salvos com sucesso em: {caminho_saida1}")
        print(f"Estatísticas salvas com sucesso em: {caminho_saida2}")
        print(f"Estatísticas globais salvas com sucesso em: {caminho_saida3}")
    except Exception as e:
        print(f"\nErro ao processar o arquivo: {str(e)}")