import os
from pathlib import Path

def processar_subpasta(subpasta_origem, palavras_por_arquivo, pasta_destino_base):
    """
    Processa uma subpasta individual com arquivos TXT, mantendo a formatação das linhas e cortando linhas se necessário.
    """
    # Obter nome da subpasta (removendo @ se necessário)
    nome_subpasta = os.path.basename(subpasta_origem)
    nome_base = nome_subpasta.replace('@', '')  # Remove o @ do nome do arquivo

    # Criar pasta de destino com mesmo nome
    pasta_destino = os.path.join(pasta_destino_base, nome_subpasta)
    os.makedirs(pasta_destino, exist_ok=True)

    # Ler e concatenar todos os TXTs, mantendo as quebras de linha
    conteudo_completo = ""
    for arquivo in os.listdir(subpasta_origem):
        if arquivo.lower().endswith('.txt'):
            caminho = os.path.join(subpasta_origem, arquivo)
            try:
                with open(caminho, 'r', encoding='utf-8') as f:
                    conteudo_completo += f.read()  # Lê o arquivo inteiro de uma vez
            except Exception as e:
                print(f"  Erro ao ler {arquivo}: {str(e)}")

    if not conteudo_completo:
        print(f"  Nenhum TXT válido encontrado em {nome_subpasta}")
        return

    linhas = conteudo_completo.splitlines(keepends=True)  # Divide o texto em linhas, mantendo as quebras
    total_palavras = len(conteudo_completo.split())  # Contagem total de palavras (aproximada)
    num_arquivos = (total_palavras + palavras_por_arquivo - 1) // palavras_por_arquivo
    
    arquivo_atual = ""
    palavras_no_arquivo_atual = 0
    arquivo_index = 1

    for linha in linhas:
        palavras_linha = linha.split()
        num_palavras_linha = len(palavras_linha)
        
        if palavras_no_arquivo_atual + num_palavras_linha > palavras_por_arquivo and arquivo_atual:
            # Se adicionar a linha exceder o limite, corta a linha e salva o arquivo
            palavras_permitidas = palavras_por_arquivo - palavras_no_arquivo_atual
            linha_cortada = " ".join(palavras_linha[:palavras_permitidas]) + '\n'  # Mantém a quebra de linha
            arquivo_atual += linha_cortada
            
            nome_arquivo = f"{nome_base}_{arquivo_index:03d}.txt"
            caminho_saida = os.path.join(pasta_destino, nome_arquivo)
            with open(caminho_saida, 'w', encoding='utf-8') as f:
                f.write(arquivo_atual)
            
            arquivo_atual = " ".join(palavras_linha[palavras_permitidas:]) + '\n' # Inicia novo arquivo com o restante da linha
            palavras_no_arquivo_atual = num_palavras_linha - palavras_permitidas
            arquivo_index += 1

        elif palavras_no_arquivo_atual + num_palavras_linha == palavras_por_arquivo:
            # Se adicionar a linha atingir exatamente o limite, adiciona a linha e salva o arquivo
            arquivo_atual += linha
            nome_arquivo = f"{nome_base}_{arquivo_index:03d}.txt"
            caminho_saida = os.path.join(pasta_destino, nome_arquivo)
            with open(caminho_saida, 'w', encoding='utf-8') as f:
                f.write(arquivo_atual)
            arquivo_atual = ""
            palavras_no_arquivo_atual = 0
            arquivo_index += 1
            
        else:
            # Se adicionar a linha não exceder o limite, apenas adiciona
            arquivo_atual += linha
            palavras_no_arquivo_atual += num_palavras_linha

    # Salva o último arquivo (se houver conteúdo)
    if arquivo_atual:
        nome_arquivo = f"{nome_base}_{arquivo_index:03d}.txt"
        caminho_saida = os.path.join(pasta_destino, nome_arquivo)
        with open(caminho_saida, 'w', encoding='utf-8') as f:
            f.write(arquivo_atual)

    print(f"  {nome_subpasta}: {arquivo_index} arquivos criados")


def processar_pasta_principal(pasta_origem, palavras_por_arquivo):
    """
    Processa todas as subpastas na pasta principal.
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