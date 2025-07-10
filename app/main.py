import streamlit as st
import pandas as pd
from filtros import inicializar_estado_sessao, sidebar_filtros, aplicar_filtros
from tabs_visao_geral import tab_visao_geral
from tabs_status import tab_status
from tabs_tabela import tab_tabela
from tabs_mapas import tab_mapas
from tabs_nuvem import tab_nuvem

# Configuração da página e sidebar mais larga
st.set_page_config(page_title="Dashboard Reclame Aqui", layout="wide")

st.markdown(
    """
    <style>
    /* Largura da sidebar */
    [data-testid="stSidebar"] {
        width: 320px;
        min-width: 320px;
    }
    [data-testid="stSidebar"] > div:first-child {
        width: 320px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

@st.cache_data
def carregar_dados():
    df = pd.read_csv("data/RECLAMEAQUI_PAODEACUCAR.csv")
    df['Cidade'] = df['LOCAL'].str.split(' - ').str[0].str.strip().str.title()
    df['UF'] = df['LOCAL'].str.split(' - ').str[1].str.strip().str.upper()
    df['STATUS'] = df['STATUS'].str.strip()
    return df

df = carregar_dados()

inicializar_estado_sessao()
sidebar_filtros(df)

df_filtrado = aplicar_filtros(df)

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Visão Geral", 
    "Status das Reclamações", 
    "Tabela de Reclamações", 
    "Mapas", 
    "Nuvem de Palavras"
])

tab_visao_geral(df_filtrado, tab1)
tab_status(df_filtrado, tab2)
tab_tabela(df_filtrado, tab3)
tab_mapas(df_filtrado, tab4)
tab_nuvem(df_filtrado, tab5)
