import os
from pathlib import Path

def processar_subpasta(subpasta_origem, palavras_por_arquivo, pasta_destino_base):
    """
    Processa uma subpasta individual com arquivos TXT, preservando quebras de linha
    """
    # Obter nome da subpasta (removendo @ se necessário)
    nome_subpasta = os.path.basename(subpasta_origem)
    nome_base = nome_subpasta.replace('@', '')  # Remove o @ do nome do arquivo
    
    # Criar pasta de destino com mesmo nome
    pasta_destino = os.path.join(pasta_destino_base, nome_subpasta)
    os.makedirs(pasta_destino, exist_ok=True)
    
    # Ler e concatenar todos os TXTs preservando quebras de linha
    conteudo_completo = []
    for arquivo in os.listdir(subpasta_origem):
        if arquivo.lower().endswith('.txt'):
            caminho = os.path.join(subpasta_origem, arquivo)
            try:
                with open(caminho, 'r', encoding='utf-8') as f:
                    # Mantém as quebras de linha originais
                    conteudo = f.read()
                    # Adiciona espaço no final se não tiver
                    if conteudo and not conteudo[-1].isspace():
                        conteudo += ' '
                    conteudo_completo.append(conteudo)
            except Exception as e:
                print(f"  Erro ao ler {arquivo}: {str(e)}")
    
    if not conteudo_completo:
        print(f"  Nenhum TXT válido encontrado em {nome_subpasta}")
        return
    
    texto_unificado = ''.join(conteudo_completo)
    
    # Processamento especial para preservar quebras ao dividir
    partes = []
    palavras = []
    contador_palavras = 0
    
    for linha in texto_unificado.splitlines(keepends=True):
        palavras_linha = linha.split()
        if not palavras_linha:
            continue
            
        for palavra in palavras_linha:
            palavras.append(palavra)
            contador_palavras += 1
            
            if contador_palavras >= palavras_por_arquivo:
                partes.append(' '.join(palavras))
                palavras = []
                contador_palavras = 0
    
    # Adiciona o restante se houver
    if palavras:
        partes.append(' '.join(palavras))
    
    # Salvar as partes
    for i, parte in enumerate(partes, start=1):
        nome_arquivo = f"{nome_base}_{i:03d}.txt"
        caminho_saida = os.path.join(pasta_destino, nome_arquivo)
        
        with open(caminho_saida, 'w', encoding='utf-8') as f:
            f.write(parte)
    
    print(f"  {nome_subpasta}: {len(partes)} arquivos criados")

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