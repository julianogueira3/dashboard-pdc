import streamlit as st
import geopandas as gpd
import folium
from streamlit_folium import st_folium
import zipfile
import os

@st.cache_data(show_spinner=False)
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

def tab_mapas(df, container):
    with container:
        st.header("Mapa Interativo de Reclamações por Estado (UF)")

        gdf_estados = carregar_shapefile_ibge()

        df_freq_uf = df.groupby('UF').size().reset_index(name='Reclamações')

        gdf_estados = gdf_estados.rename(columns={'SIGLA_UF': 'UF'})
        gdf_merged = gdf_estados.merge(df_freq_uf, on='UF', how='left').fillna(0)

        def criar_tooltip(row):
            return f"{row['NM_UF']} ({row['UF']}): {int(row['Reclamações'])} reclamações"
        gdf_merged['tooltip'] = gdf_merged.apply(criar_tooltip, axis=1)

        m = folium.Map(location=[-15.78, -47.93], zoom_start=4)

        max_reclamacoes = gdf_merged['Reclamações'].max()
        choropleth = folium.Choropleth(
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
                'fillColor': '#transparent',
                'color': 'black',
                'weight': 0.5,
                'fillOpacity': 0
            },
            tooltip=folium.GeoJsonTooltip(fields=['tooltip'], labels=False)
        ).add_to(m)

        st_folium(m, width=700, height=500)
