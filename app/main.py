import streamlit as st
import pandas as pd
from tabs_visao_geral import tab_visao_geral
from tabs_status import tab_status
from tabs_tabela import tab_tabela
from tabs_mapas import tab_mapas
from tabs_nuvem import tab_nuvem

# Carregar dados (único ponto)
@st.cache_data
def carregar_dados():
    df = pd.read_csv("data/RECLAMEAQUI_PAODEACUCAR.csv")
    df['Cidade'] = df['LOCAL'].str.split(' - ').str[0].str.strip().str.title()
    df['UF'] = df['LOCAL'].str.split(' - ').str[1].str.strip().str.upper()
    df['STATUS'] = df['STATUS'].str.strip()
    return df

df = carregar_dados()

# Inicializar estado da sessão
for key, default in {
    "estados": [],
    "cidades": [],
    "status": [],
    "min_estado": 1,
    "min_cidade": 1,
    "top_n": 5,
}.items():
    if key not in st.session_state:
        st.session_state[key] = default

# CSS
st.markdown("""
<style>
/* Ajusta todos os botões dentro das colunas da sidebar */
section[data-testid="stSidebar"] div[data-testid="column"] button {
    width: 100% !important;
    padding: 0.5rem 0 !important;
    font-size: 0.85rem !important;
}
</style>
""", unsafe_allow_html=True)

# Sidebar
st.sidebar.header("Filtros Interativos")

# Funções para manipular filtros
def selecionar_todos_estados():
    st.session_state.estados = sorted(df['UF'].unique())

def limpar_estados():
    st.session_state.estados = []

def selecionar_todas_cidades():
    cidades_disponiveis = obter_cidades_disponiveis()
    st.session_state.cidades = cidades_disponiveis

def limpar_cidades():
    st.session_state.cidades = []

def selecionar_todos_status():
    st.session_state.status = sorted(df['STATUS'].unique())

def limpar_status():
    st.session_state.status = []

def limpar_tudo():
    limpar_estados()
    limpar_cidades()
    limpar_status()
    st.session_state.min_estado = 1
    st.session_state.min_cidade = 1
    st.session_state.top_n = 5

def obter_cidades_disponiveis():
    if st.session_state.estados:
        cidades = df[df['UF'].isin(st.session_state.estados)]['Cidade'].unique()
    else:
        cidades = df['Cidade'].unique()
    return sorted(cidades)

if st.sidebar.button("Limpar todos os filtros", key="btn_limpar_tudo"):
    limpar_tudo()

with st.sidebar.expander("Estado", expanded=True):
    estados_disponiveis = sorted(df['UF'].unique())
    col1, col2 = st.columns([1, 1])
    with col1:
        st.button("Selecionar todos", on_click=selecionar_todos_estados, key="btn_sel_todos_estados")
    with col2:
        st.button("Limpar", on_click=limpar_estados, key="btn_limpar_estados")
    st.multiselect(
        "Selecione Estado(s):",
        options=estados_disponiveis,
        default=st.session_state.estados,
        key="estados"
    )
    st.slider(
        "Mínimo de Reclamações por Estado",
        min_value=1,
        max_value=100,
        value=st.session_state.min_estado,
        key="min_estado"
    )

with st.sidebar.expander("Cidade", expanded=True):
    cidades_disponiveis = obter_cidades_disponiveis()
    col1, col2 = st.columns([1, 1])
    with col1:
        st.button("Selecionar todas", on_click=selecionar_todas_cidades, key="btn_sel_todas_cidades")
    with col2:
        st.button("Limpar", on_click=limpar_cidades, key="btn_limpar_cidades")
    st.multiselect(
        "Selecione Cidade(s):",
        options=cidades_disponiveis,
        default=st.session_state.cidades,
        key="cidades"
    )
    st.slider(
        "Mínimo de Reclamações por Cidade",
        min_value=1,
        max_value=100,
        value=st.session_state.min_cidade,
        key="min_cidade"
    )

with st.sidebar.expander("Status", expanded=True):
    status_disponiveis = sorted(df['STATUS'].unique())
    col1, col2 = st.columns([1, 1])
    with col1:
        st.button("Selecionar todos", on_click=selecionar_todos_status, key="btn_sel_todos_status")
    with col2:
        st.button("Limpar", on_click=limpar_status, key="btn_limpar_status")
    st.multiselect(
        "Selecione Status:",
        options=status_disponiveis,
        default=st.session_state.status,
        key="status"
    )

top_options = [5, 10, 15, 20, 'Todos']
top_n = st.sidebar.selectbox(
    "Quantidade de Top para gráficos",
    options=top_options,
    index=0,
    key="top_n"
)
top_n_int = 999999 if top_n == 'Todos' else top_n

# Filtrar dataframe com os filtros escolhidos
df_filtrado = df.copy()
if st.session_state.estados:
    df_filtrado = df_filtrado[df_filtrado['UF'].isin(st.session_state.estados)]
if st.session_state.cidades:
    df_filtrado = df_filtrado[df_filtrado['Cidade'].isin(st.session_state.cidades)]
if st.session_state.status:
    df_filtrado = df_filtrado[df_filtrado['STATUS'].isin(st.session_state.status)]

# Aplicar filtro mínimo por estado e cidade
estado_counts = df_filtrado['UF'].value_counts()
cidade_counts = df_filtrado['Cidade'].value_counts()
estados_validos = estado_counts[estado_counts >= st.session_state.min_estado].index.tolist()
cidades_validas = cidade_counts[cidade_counts >= st.session_state.min_cidade].index.tolist()

df_filtrado = df_filtrado[
    (df_filtrado['UF'].isin(estados_validos)) &
    (df_filtrado['Cidade'].isin(cidades_validas))
]

# Tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Visão Geral", 
    "Status das Reclamações", 
    "Tabela de Reclamações", 
    "Mapas", 
    "Nuvem de Palavras"
])

tab_visao_geral(df_filtrado, top_n_int, tab1)
tab_status(df_filtrado, tab2)
tab_tabela(df_filtrado, tab3)
tab_mapas(df_filtrado, tab4)
tab_nuvem(df_filtrado, tab5)

