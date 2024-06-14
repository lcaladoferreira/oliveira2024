import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static
import matplotlib.pyplot as plt
import numpy as np



st.set_page_config(layout="wide", page_title="Oliveira 2024", page_icon="🇧🇷")
# Configurando o título e o favicon



# Dados das zonas, votos em cada ano e endereços
zonas = ['ZE 328', 'ZE 373', 'ZE 372', 'ZE 381', 'ZE 408', 'ZE 246', 'ZE 351', 'ZE 280']
votos_2006 = [2474, 2194, 1751, 1733, 1508, 1398, 1228, 1132]
votos_2008 = [2743, 2035, 1973, 1743, 1306, 1302, 1138, 705]
votos_2012 = [2255, 1617, 1170, 939, 870, 845, 694, 652]
enderecos = [
    'R. Américo Falcão, 251 - Vila Pirajussara, São Paulo - SP, 05786-010, Brazil',
    'Estr. de Itapecerica, 2.720 - Capao Redondo, São Paulo - SP, 05835-004, Brazil',
    'R. Prof. Barroso do Amaral, 32 - Jardim Angela (Zona Sul), São Paulo - SP, 04948-030, Brazil',
    'Av. Pedro Roschel Gottsfritz, 210 - Rio Bonito, São Paulo - SP, 04809-160, Brazil',
    'Térreo, R. Américo Falcão, 251 - Vila Pirajussara, São Paulo - SP, 05786-010, Brazil',
    'R. Tenente-Coronel Carlos da Silva Araújo, 355 - Santo Amaro, São Paulo - SP, 04751-050, Brazil',
    'Av. Cupecê, 1147 - Jardim Prudência, São Paulo - SP, 04365-000, Brazil',
    'Av. Atlântica, 1551 - Veleiros, São Paulo - SP, 04768-200, Brazil'
]
latitudes = [-23.621693, -23.670302, -23.676885, -23.696234, -23.621693, -23.646634, -23.661232, -23.671344]
longitudes = [-46.738166, -46.654888, -46.747349, -46.670375, -46.738166, -46.779775, -46.668882, -46.700665]

# Criação do DataFrame
data = {
    'Zona': zonas,
    'Endereço': enderecos,
    'Latitude': latitudes,
    'Longitude': longitudes,
    '2006': votos_2006,
    '2008': votos_2008,
    '2012': votos_2012
}
df = pd.DataFrame(data)

# Remover as colunas de latitude e longitude do DataFrame
df_display = df.drop(columns=['Latitude', 'Longitude'])

# Título da aplicação
st.title('As 8 zonas eleitorais mais Votadas das Eleições de 2006, 2008 e 2012:')

# Seleção de anos e zonas na barra lateral
with st.sidebar:
    st.subheader('Selecione os Anos:')
    anos_2006 = st.checkbox('Eleições de 2006', True)
    anos_2008 = st.checkbox('Eleições de 2008', True)
    anos_2012 = st.checkbox('Eleições de 2012', True)

    zonas_selecionadas = st.multiselect('Selecione as zonas:', zonas, default=zonas)

# Filtrar o DataFrame de acordo com a seleção
df_filtrado = df[df['Zona'].isin(zonas_selecionadas)]

# Layout em colunas
col1, _ = st.columns([3, 1])

# Plotagem do gráfico de barras
with col1:
    st.subheader('Gráfico de Barras - Popularidade das Zonas em Diferentes Anos')
    # Plotagem dos dados filtrados
    fig, ax = plt.subplots(figsize=(6, len(df_filtrado) * 0.5))

    # Cores para os diferentes anos
    cores = {
        '2006': 'skyblue',
        '2008': 'orange',
        '2012': 'green'
    }

    bar_width = 0.2  # Largura das barras
    space_between_bars = 0.1  # Espaço entre as barras
    for i, ano in enumerate(['2006', '2008', '2012']):
        if eval(f'anos_{ano}'):
            bars = ax.bar(np.arange(len(df_filtrado)) + i * (bar_width + space_between_bars), df_filtrado[ano], bar_width, label=f'Votos em {ano}', color=cores[ano])
            # Adiciona o texto com a quantidade de votos em cada barra
            for j, bar in enumerate(bars):
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2, height * 1.01, f'{int(height)}', ha='center', va='bottom', fontsize=8)

    # Adiciona o nome das zonas na parte inferior do gráfico
    ax.set_xticks(np.arange(len(df_filtrado)) + (bar_width + space_between_bars) * 1.5)
    ax.set_xticklabels(df_filtrado['Zona'], rotation=45, ha='right', fontsize=8)

    # Configurações do gráfico
    ax.set_yticks([])
    ax.legend()

    # Exibição do gráfico
    st.pyplot(fig)

    # Exibição da tabela com endereços
    st.subheader('Tabela de Votos e Endereços das Zonas Selecionadas:')
    # Centraliza a tabela dentro do container
    st.write(df_display.set_index('Zona'))


# Título da aplicação
st.title('Mapa das Zonas Eleitorais Selecionadas:')
# Mapa dos locais de votação
mapa = folium.Map(location=[-23.642885, -46.730349], zoom_start=12)  # São Paulo para inicialização do mapa

# Adicionar círculos proporcionais ao número de votos no mapa
for _, row in df_filtrado.iterrows():
    for i, ano in enumerate(['2006', '2008', '2012']):
        if eval(f'anos_{ano}'):
            folium.Circle(
                location=[row['Latitude'], row['Longitude']],
                radius=row[ano] * 0.4,  # Ajustar o fator conforme necessário para o tamanho dos círculos
                color=cores[ano],
                fill=True,
                fill_color=cores[ano],
                fill_opacity=0.3,
                popup=f"<b>{row['Zona']}</b><br>{row['Endereço']}<br>Votos em {ano}: {row[ano]}"
            ).add_to(mapa)

# Exibição do mapa
folium_static(mapa)

# Dados dos votos por ano
anos = ['2006', '2008', '2012']
votos = [18203, 19003, 14059]

# Plotagem do gráfico de barras
st.title('Histórico Total de Votos (2006-2012)')
fig, ax = plt.subplots(figsize=(9, 3))  # Defina o tamanho do gráfico aqui

# Cores para os diferentes anos
cores = {
    '2006': 'skyblue',
    '2008': 'orange',
    '2012': 'green'
}

# Largura das barras
bar_width = 0.5

# Plotagem das barras
for i, ano in enumerate(anos):
    ax.bar(ano, votos[i], color=cores[ano], width=bar_width)

# Adicionando os números acima de cada barra
for i, ano in enumerate(anos):
    height = votos[i]
    ax.text(ano, height * 0.9, int(height), ha='center', va='bottom')

# Removendo o eixo X
ax.set_yticks([])

# Exibição do gráfico
st.pyplot(fig)

st.title('Mapa Detalhado do Total de Votos por Zona Eleitoral (2006-2012)')
# Adicionando o iframe do Google Maps
iframe_html = '<iframe src="https://www.google.com/maps/d/embed?mid=1BolAS64jMrPqGfc5YVhLG5vOiklmF3A&ehbc=2E312F&noprof=1" width="900" height="900"></iframe>'
st.components.v1.html(iframe_html, width=900, height=900)
