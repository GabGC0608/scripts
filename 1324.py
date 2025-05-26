import os
from pathlib import Path

def processar_subpasta(subpasta_origem, palavras_por_arquivo, pasta_destino_base):
    """
    Processa uma subpasta individual com arquivos TXT
    """
    # Obter nome da subpasta (removendo @ se necessário)
    nome_subpasta = os.path.basename(subpasta_origem)
    nome_base = nome_subpasta.replace('@', '')  # Remove o @ do nome do arquivo
    
    # Criar pasta de destino com mesmo nome
    pasta_destino = os.path.join(pasta_destino_base, nome_subpasta)
    os.makedirs(pasta_destino, exist_ok=True)
    
    # Ler e concatenar todos os TXTs sem quebras de linha
    conteudo_completo = []
    for arquivo in os.listdir(subpasta_origem):
        if arquivo.lower().endswith('.txt'):
            caminho = os.path.join(subpasta_origem, arquivo)
            try:
                with open(caminho, 'r', encoding='utf-8') as f:
                    # Lê todo o conteúdo, remove quebras de linha e espaços extras
                    texto = f.read().replace('\n', ' ').replace('\r', '')
                    # Remove espaços múltiplos e adiciona um espaço no final
                    texto_limpo = ' '.join(texto.split()) + ' '
                    conteudo_completo.append(texto_limpo)
            except Exception as e:
                print(f"  Erro ao ler {arquivo}: {str(e)}")
    
    if not conteudo_completo:
        print(f"  Nenhum TXT válido encontrado em {nome_subpasta}")
        return
    
    texto_unificado = ''.join(conteudo_completo)
    palavras = texto_unificado.split()
    total_palavras = len(palavras)
    
    # Dividir em partes
    num_arquivos = (total_palavras + palavras_por_arquivo - 1) // palavras_por_arquivo
    
    for i in range(num_arquivos):
        inicio = i * palavras_por_arquivo
        fim = min((i + 1) * palavras_por_arquivo, total_palavras)
        parte = ' '.join(palavras[inicio:fim])
        
        # Nome do arquivo com nome da pasta + número
        nome_arquivo = f"{nome_base}_{i+1:03d}.txt"  # Formato: nomedapasta_001.txt
        caminho_saida = os.path.join(pasta_destino, nome_arquivo)
        
        with open(caminho_saida, 'w', encoding='utf-8') as f:
            f.write(parte)
    
    print(f"  {nome_subpasta}: {num_arquivos} arquivos criados")

def processar_pasta_principal(pasta_origem, palavras_por_arquivo):
    """
    Processa todas as subpastas na pasta principal
    """
    print("\nIniciando processamento...")
    
    # Criar pasta base de destino
    pasta_destino_base = os.path.join(pasta_origem, "TXT_DIVIDIDOS")
    os.makedirs(pasta_destino_base, exist_ok=True)
    
    # Processar cada subpasta
    for item in os.listdir(pasta_origem):
        caminho_completo = os.path.join(pasta_origem, item)
        if item.startswith('@') and os.path.isdir(caminho_completo):
            processar_subpasta(caminho_completo, palavras_por_arquivo, pasta_destino_base)
    
    return pasta_destino_base

def main():
    print("=== DIVISOR DE TXTs EM SUBPASTAS ===")
    print("Processa todas as subpastas com nomes começando em @\n")
    
    # Configurar diretório
    pasta_origem = 'C:/Users/Gabriel/Desktop/Artigo_atualizado/_comentarios_txt'
    while not os.path.isdir(pasta_origem):
        print("Diretório não encontrado!")
        pasta_origem = input("Digite novamente: ").strip()
    
    # Configurar número de palavras (fixo em 300)
    palavras_por_arquivo = 300
    
    # Processar
    destino = processar_pasta_principal(pasta_origem, palavras_por_arquivo)
    
    # Resultado
    print("\nProcesso concluído com sucesso!")
    print(f"Arquivos divididos salvos em: {os.path.abspath(destino)}")

if __name__ == "__main__":
    main() 