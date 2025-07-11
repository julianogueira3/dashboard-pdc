import streamlit as st
import geopandas as gpd
import pandas as pd
import folium
import zipfile
import os
from streamlit_folium import st_folium

@st.cache_resource(show_spinner=False)
def carregar_shapefile_ibge():
    url = 'https://geoftp.ibge.gov.br/organizacao_do_territorio/malhas_territoriais/malhas_municipais/municipio_2024/Brasil/BR_UF_2024.zip'
    zip_path = 'BR_UF_2024.zip'
    extract_folder = 'shapefile_ibge'

    if not os.path.exists(zip_path):
        import wget
        wget.download(url, zip_path)

    if not os.path.exists(extract_folder):
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_folder)

    shapefile_path = os.path.join(extract_folder, 'BR_UF_2024.shp')
    gdf = gpd.read_file(shapefile_path)
    return gdf

def mapa_por_total(df, gdf_estados):
    df_freq_uf = df.groupby('UF').size().reset_index(name='Reclamações')
    gdf_estados = gdf_estados.rename(columns={'SIGLA_UF': 'UF'})
    gdf_merged = gdf_estados.merge(df_freq_uf, on='UF', how='left').fillna(0)

    gdf_merged['tooltip'] = gdf_merged.apply(
        lambda row: f"{row['NM_UF']} ({row['UF']}): {int(row['Reclamações'])} reclamações", axis=1
    )

    m = folium.Map(location=[-15.78, -47.93], zoom_start=4)

    max_reclamacoes = gdf_merged['Reclamações'].max()
    folium.Choropleth(
        geo_data=gdf_merged,
        name="choropleth",
        data=gdf_merged,
        columns=['UF', 'Reclamações'],
        key_on='feature.properties.UF',
        fill_color='YlOrRd',
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name='Quantidade de Reclamações',
        threshold_scale=[0, max_reclamacoes*0.25, max_reclamacoes*0.5, max_reclamacoes*0.75, max_reclamacoes],
        reset=True
    ).add_to(m)

    folium.GeoJson(
        gdf_merged,
        style_function=lambda feature: {
            'fillColor': 'transparent',
            'color': 'black',
            'weight': 0.5,
            'fillOpacity': 0
        },
        tooltip=folium.GeoJsonTooltip(fields=['tooltip'], labels=False)
    ).add_to(m)

    return m

def mapa_por_status(df, gdf_estados):
    df_freq = df.groupby(['UF', 'STATUS']).size().reset_index(name='Frequência')
    df_pivot = df_freq.pivot(index='UF', columns='STATUS', values='Frequência').fillna(0).reset_index()

    gdf_estados = gdf_estados.rename(columns={'SIGLA_UF': 'UF'})
    gdf_merged = gdf_estados.merge(df_pivot, on='UF', how='left').fillna(0)

    def criar_tooltip(row):
        textos = []
        for status in df_freq['STATUS'].unique():
            textos.append(f"{status}: {int(row.get(status, 0))}")
        return '<br>'.join(textos)

    gdf_merged['tooltip'] = gdf_merged.apply(criar_tooltip, axis=1)

    m = folium.Map(location=[-15.78, -47.93], zoom_start=4)

    folium.GeoJson(
        gdf_merged,
        style_function=lambda feature: {
            'fillColor': '#3186cc',
            'color': 'black',
            'weight': 1,
            'fillOpacity': 0.6,
        },
        tooltip=folium.GeoJsonTooltip(
            fields=['tooltip'],
            labels=False,
            sticky=True
        )
    ).add_to(m)

    return m

def mapa_por_categoria(df, gdf_estados):
    # Preparar dados para categorias
    df['UF'] = df['LOCAL'].str.split(' - ').str[1].str.strip().str.upper()
    df_explodido = df.assign(
        CATEGORIA_SEPARADA = df['CATEGORIA'].str.split('<->')
    ).explode('CATEGORIA_SEPARADA')

    indesejadas = ['Supermercados', 'Pão de Açúcar', 'Não encontrei meu problema', 'Hipermercados']
    df_filtrado = df_explodido[~df_explodido['CATEGORIA_SEPARADA'].isin(indesejadas)]

    categorias_validas = df_filtrado['CATEGORIA_SEPARADA'].unique()
    df_freq = df_filtrado.groupby(['UF', 'CATEGORIA_SEPARADA']).size().reset_index(name='Frequência')
    df_pivot = df_freq.pivot(index='UF', columns='CATEGORIA_SEPARADA', values='Frequência').fillna(0).reset_index()

    gdf_estados = gdf_estados.rename(columns={'SIGLA_UF': 'UF'})
    gdf_merged = gdf_estados.merge(df_pivot, on='UF', how='left').fillna(0)

    def criar_tooltip(row):
        textos = []
        for categoria in categorias_validas:
            freq = int(row.get(categoria, 0))
            if freq > 0:
                textos.append(f"{categoria}: {freq}")
        return '<br>'.join(textos) if textos else 'Sem dados'

    gdf_merged['tooltip'] = gdf_merged.apply(criar_tooltip, axis=1)

    m = folium.Map(location=[-15.78, -47.93], zoom_start=4)

    folium.GeoJson(
        gdf_merged,
        style_function=lambda feature: {
            'fillColor': '#3186cc',
            'color': 'black',
            'weight': 1,
            'fillOpacity': 0.6,
        },
        tooltip=folium.GeoJsonTooltip(
            fields=['tooltip'],
            labels=False,
            sticky=True
        )
    ).add_to(m)

    return m

def tab_mapas(df, container):
    with container:
        st.header("🗺️ Mapa Interativo de Reclamações por Estado (UF)")

        col1, col2 = st.columns([1, 3])

    
        with col1:
            opcao = st.selectbox(
                "Selecione o tipo de mapa:",
                ["Total por UF", "Por Status", "Por Categoria"],
                key="mapa_tipo"
            )

        with col2:
            
            df['Ano'] = pd.to_datetime(df['TEMPO'], errors='coerce').dt.year.dropna().astype(int)
            anos_disponiveis = sorted(df['Ano'].dropna().unique())
            ano_selecionado = st.selectbox("Selecione o ano:", anos_disponiveis, index=len(anos_disponiveis) - 1)
            df = df[df['Ano'] == ano_selecionado]

            gdf_estados = carregar_shapefile_ibge()
            if opcao == "Total por UF":
                mapa = mapa_por_total(df.copy(), gdf_estados.copy())
                st.subheader("Total de Reclamações por Estado")
            elif opcao == "Por Status":
                mapa = mapa_por_status(df.copy(), gdf_estados.copy())
                st.subheader("Reclamações por Status")
            else:
                mapa = mapa_por_categoria(df.copy(), gdf_estados.copy())
                st.subheader("Reclamações por Categoria")

            st_folium(mapa, width=700, height=500)
