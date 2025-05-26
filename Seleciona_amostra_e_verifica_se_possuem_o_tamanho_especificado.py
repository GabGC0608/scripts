import os
import random
import shutil

def contar_palavras(arquivo_path):
    """Conta o número de palavras em um arquivo TXT (exatamente 300 palavras)."""
    try:
        with open(arquivo_path, 'r', encoding='utf-8') as f:
            conteudo = f.read()
            palavras = conteudo.split()
            return len(palavras)
    except Exception as e:
        print(f"  Erro ao ler {arquivo_path}: {str(e)}")
        return -1  # Retorna -1 em caso de erro

def selecionar_amostras(pasta_origem, pasta_destino, amostras_por_pasta):
    """
    Seleciona X arquivos aleatórios de cada subpasta (com EXATAMENTE 300 palavras)
    e copia para a pasta destino.
    """
    # Garantir que a pasta de destino existe
    os.makedirs(pasta_destino, exist_ok=True)
    
    # Processar cada subpasta que começa com @
    for item in os.listdir(pasta_origem):
        caminho_subpasta = os.path.join(pasta_origem, item)
        
        if item.startswith('@') and os.path.isdir(caminho_subpasta):
            print(f"\nProcessando: {item}")
            
            # Listar todos os arquivos TXT
            arquivos_txt = [f for f in os.listdir(caminho_subpasta) 
                          if f.lower().endswith('.txt')]
            
            if not arquivos_txt:
                print(f"  Nenhum arquivo TXT encontrado em {item}")
                continue
                
            # Preparar para seleção aleatória com verificação
            amostras_selecionadas = []
            tentativas = 0
            max_tentativas = len(arquivos_txt) * 3  # Limite de tentativas
            
            while len(amostras_selecionadas) < amostras_por_pasta and tentativas < max_tentativas:
                # Escolher um arquivo aleatório
                arquivo = random.choice(arquivos_txt)
                caminho_arquivo = os.path.join(caminho_subpasta, arquivo)
                
                # Verificar se tem EXATAMENTE 300 palavras
                num_palavras = contar_palavras(caminho_arquivo)
                
                if num_palavras == 300:
                    if arquivo not in amostras_selecionadas:  # Evitar duplicatas
                        amostras_selecionadas.append(arquivo)
                        print(f"   Selecionado (300 palavras): {arquivo}")
                else:
                    print(f"   Ignorado ({num_palavras} palavras): {arquivo}")
                
                tentativas += 1
            
            # Verificar se conseguiu amostras suficientes
            if not amostras_selecionadas:
                print(f"   Nenhum arquivo com exatamente 300 palavras em {item}")
                continue
                
            # Copiar cada arquivo selecionado
            for arquivo in amostras_selecionadas:
                origem = os.path.join(caminho_subpasta, arquivo)
                destino = os.path.join(pasta_destino, f"{item}_{arquivo}")
                
                try:
                    shutil.copy2(origem, destino)
                except Exception as e:
                    print(f"   Erro ao copiar {arquivo}: {str(e)}")

def main():
    print("=== SELETOR ALEATÓRIO DE AMOSTRAS ===")
    print("Seleciona X arquivos TXT com EXATAMENTE 300 palavras de cada subpasta (@)\n")
    
    # Configurar diretórios
    pasta_origem = 'C:/Users/Gabriel/Desktop/Artigo_atualizado/_comentarios_txt/TXT_DIVIDIDOS'
    while not os.path.isdir(pasta_origem):
        print("Diretório não encontrado!")
        pasta_origem = input("Digite novamente: ").strip()
    
    pasta_destino = os.path.join(pasta_origem, "AMOSTRAS_300_PALAVRAS")
    
    # Configurar número de amostras
    amostras_por_pasta = 8  # Definido como 9, mas pode ser ajustado
    
    # Processar
    selecionar_amostras(pasta_origem, pasta_destino, amostras_por_pasta)
    
    # Resultado
    print("\n Processo concluído!")
    print(f" Amostras salvas em: {os.path.abspath(pasta_destino)}")

if __name__ == "__main__":
    main()