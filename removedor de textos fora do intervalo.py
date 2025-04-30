import os

def contar_palavras(arquivo):
    with open(arquivo, "r", encoding="utf-8-sig") as f:
        return len(f.read().split())

def remover_textos_por_tamanho(pasta, min_palavras, max_palavras):
    for raiz, _, arquivos in os.walk(pasta):
        for arquivo in arquivos:
            if arquivo.endswith(".txt"):
                caminho_arquivo = os.path.join(raiz, arquivo)
                num_palavras = contar_palavras(caminho_arquivo)
                
                if num_palavras < min_palavras or num_palavras > max_palavras:
                    os.remove(caminho_arquivo)
                    print(f"Removido: {caminho_arquivo} ({num_palavras} palavras)")

# Configurações
# Defina o caminho da pasta onde estão os textos
pasta_base = "C:/Users/Gabriel/Desktop/teste_artigo/MEU/removendo os 0/pastas dos canais/@RBtechinfo"

# Defina o intervalo de palavras que os arquivos devem obedecer
min_palavras = 250  # Limite mínimo de palavras
max_palavras = 464  # Limite máximo de palavras

remover_textos_por_tamanho(pasta_base, min_palavras, max_palavras)
