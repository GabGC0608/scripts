import os
import shutil

def agrupar_arquivos(pasta_origem, pasta_destino, numero_pastas=49):
    """
    Percorre um número especificado de pastas e agrupa todos os arquivos em uma pasta de destino.

    Parâmetros:
    pasta_origem (str): Caminho da pasta principal contendo as subpastas.
    pasta_destino (str): Caminho da pasta onde os arquivos serão agrupados.
    numero_pastas (int): Número de pastas a serem percorridas (padrão: 50).
    """
    # Garantir que a pasta de destino exista
    if not os.path.exists(pasta_destino):
        os.makedirs(pasta_destino)

    # Listar as subpastas na pasta de origem
    subpastas = [os.path.join(pasta_origem, subpasta) for subpasta in os.listdir(pasta_origem) if os.path.isdir(os.path.join(pasta_origem, subpasta))]

    # Limitar ao número de pastas especificado
    subpastas = subpastas[:numero_pastas]

    # Percorrer cada subpasta
    for subpasta in subpastas:
        print(f"Processando pasta: {subpasta}")
        for arquivo in os.listdir(subpasta):
            caminho_arquivo = os.path.join(subpasta, arquivo)
            if os.path.isfile(caminho_arquivo):
                # Copiar o arquivo para a pasta de destino
                shutil.copy(caminho_arquivo, pasta_destino)
                print(f"Arquivo copiado: {caminho_arquivo}")

    print(f"\nTodos os arquivos foram agrupados na pasta: {pasta_destino}")

if __name__ == "__main__":
    # Caminho da pasta principal contendo as subpastas
    pasta_origem = 'C:/Users/Gabriel/Desktop/Artigo_atualizado/_comentarios_txt'

    # Caminho da pasta de destino
    pasta_destino = 'C:/Users/Gabriel/Desktop/Artigo_atualizado/corpus_agrupado'

    # Executar o agrupamento
    agrupar_arquivos(pasta_origem, pasta_destino)