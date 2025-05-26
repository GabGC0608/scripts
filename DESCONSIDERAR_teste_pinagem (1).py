import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# --- 1. Dados de exemplo ---
# df_videos: canal e contagem de comentários por vídeo
df_videos = pd.read_csv("C:/Users/Gabriel/Desktop/Artigo_atualizado/tabelas/todos_os_comentarios.csv", sep=',')
df_counts = df_videos.groupby('videoid').size().reset_index(name='comment_count')
df_videos = df_videos.merge(df_counts, on='videoid', how='left')

# --- 2. Definir bins ---
w = 20
bins = np.arange(0, df_videos['comment_count'].max() + w, w) 
df_videos['count_bin'] = pd.cut(df_videos['comment_count'], bins=bins, right=False)

# --- 3. Contar vídeos por bin e canal ---
bin_counts = (df_videos.groupby(['canal', 'count_bin'], observed=True).size().reset_index(name='count'))

# --- 4. Escolher o bin de maior densidade ---
idx = bin_counts.groupby('canal')['count'].idxmax()
max_bins = bin_counts.loc[idx].copy()

# --- 5. Calcular porcentagem ---
totals = df_videos.groupby('canal').size().rename('total_videos')
max_bins = max_bins.join(totals, on='canal')
max_bins['percentage'] = 100 * max_bins['count'] / max_bins['total_videos']

# Resultado final
print(max_bins[['canal', 'count_bin', 'count', 'percentage']])

# Contar o número de vídeos por canal em cada bin
bin_distribution = df_videos.groupby(['canal', 'count_bin'], observed=True).size().reset_index(name='video_count')

# Calcular o total de vídeos por canal
total_videos_per_canal = df_videos.groupby('canal').size().rename('total_videos').reset_index()

# Adicionar o total de vídeos por canal à tabela de distribuição
bin_distribution = bin_distribution.merge(total_videos_per_canal, on='canal')

# Calcular a porcentagem de vídeos em cada bin por canal
bin_distribution['percentage'] = (100 * bin_distribution['video_count'] / bin_distribution['total_videos']).round(2).astype(float)

# Pivot para reorganizar a tabela: um canal por linha, bins como colunas
pivot_table = bin_distribution.pivot(index='canal', columns='count_bin', values='percentage').fillna(0)

# Renomear as colunas para facilitar a leitura
pivot_table.columns = [f'Bin {col}' for col in pivot_table.columns]

# Salvar a tabela em Excel, se necessário
pivot_table.to_excel("C:/Users/Gabriel/Desktop/Artigo_atualizado/tabelas/tabela_bins.xlsx")

'''
# Boxplot para dispersão de comentários por canal (ajustado para tela Full HD)
plt.figure(figsize=(16, 9))  # Ajustar tamanho para tela Full HD
sns.boxplot(data=df_videos, x='canal', y='comment_count')  # Adicionar paleta de cores
plt.title('Dispersão de Comentários por Canal', fontsize=18)  # Aumentar tamanho do título
plt.xlabel('Canal', fontsize=12)  # Aumentar tamanho do rótulo do eixo X
plt.ylabel('Número de Comentários', fontsize=14)  # Aumentar tamanho do rótulo do eixo Y
plt.xticks(rotation=90, fontsize=10)  # Ajustar rotação e tamanho das labels do eixo X
plt.yticks(fontsize=12)  # Ajustar tamanho das labels do eixo Y
plt.tight_layout()  # Garantir que os elementos não fiquem cortados
plt.show() # Mostrar o gráfico

'''

# Pivot para criar uma tabela para gráfico de barras empilhadas
pivot = bin_distribution.pivot(index='canal', columns='count_bin', values='percentage').fillna(0)

# Gráfico de barras empilhadas
pivot.plot(kind='bar', stacked=True, figsize=(12, 6), colormap='viridis')
plt.title('Distribuição de Vídeos por Canal e Bin (%)')
plt.xlabel('Canal')
plt.ylabel('Porcentagem de Vídeos (%)')
plt.legend(title='Bins', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.show()

