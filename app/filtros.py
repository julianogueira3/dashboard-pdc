import streamlit as st
import pandas as pd


def inicializar_estado_sessao():
    defaults = {
        "estados": [],
        "cidades": [],
        "status": [],
        "min_estado": 1,
        "min_cidade": 1,
        "top_n": 5,
    }
    for key, default in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = default

def sidebar_filtros(df):
    def selecionar_todos_estados():
        st.session_state.estados = sorted(df['UF'].unique())

    def limpar_estados():
        st.session_state.estados = []

    def selecionar_todas_cidades():
        cidades_disponiveis = obter_cidades_disponiveis(df)
        st.session_state.cidades = cidades_disponiveis

    def limpar_cidades():
        st.session_state.cidades = []

    def selecionar_todos_status():
        st.session_state.status = sorted(df['STATUS'].unique())

    def limpar_status():
        st.session_state.status = []

    def limpar_datas():
        df['TEMPO'] = pd.to_datetime(df['TEMPO'])
        st.session_state.data_inicial = df['TEMPO'].min().date()
        st.session_state.data_final = df['TEMPO'].max().date()

    def limpar_tudo():
        limpar_estados()
        limpar_cidades()
        limpar_status()
        limpar_datas()

        st.session_state.min_estado = 1
        st.session_state.min_cidade = 1
        st.session_state.top_n = 5

    def obter_cidades_disponiveis(df):
        if st.session_state.estados:
            cidades = df[df['UF'].isin(st.session_state.estados)]['Cidade'].unique()
        else:
            cidades = df['Cidade'].unique()
        return sorted(cidades)

    st.sidebar.header("Filtros Interativos")

    with st.sidebar.expander("🌎 Estado", expanded=False):
        estados_disponiveis = sorted(df['UF'].unique())
        col1, col2 = st.columns([1,1])
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

    with st.sidebar.expander("🌎 Cidade", expanded=False):
        cidades_disponiveis = obter_cidades_disponiveis(df)
        col1, col2 = st.columns([1,1])
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

    with st.sidebar.expander("📌 Status", expanded=False):
        status_disponiveis = sorted(df['STATUS'].unique())
        col1, col2 = st.columns([1,1])
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

        with st.sidebar.expander("📅 Intervalo de Datas", expanded=False):
            st.button("Limpar", on_click=limpar_datas, key="btn_limpar_datas")
            df['TEMPO'] = pd.to_datetime(df['TEMPO'])

            data_min = df['TEMPO'].min().date()
            data_max = df['TEMPO'].max().date()

            col1, col2 = st.columns(2)
            with col1:
                data_inicial = st.date_input(
                    "Data Inicial",
                    value=data_min,
                    min_value=data_min,
                    max_value=data_max,
                    key="data_inicial"
                )
            with col2:
                data_final = st.date_input(
                    "Data Final",
                    value=data_max,
                    min_value=data_min,
                    max_value=data_max,
                    key="data_final"
                )


    st.sidebar.markdown("---")
    st.sidebar.button("Limpar todos os filtros", on_click=limpar_tudo, key="btn_limpar_tudo")
    

def aplicar_filtros(df):
    df_filtrado = df.copy()
    if st.session_state.estados:
        df_filtrado = df_filtrado[df_filtrado['UF'].isin(st.session_state.estados)]
    if st.session_state.cidades:
        df_filtrado = df_filtrado[df_filtrado['Cidade'].isin(st.session_state.cidades)]
    if st.session_state.status:
        df_filtrado = df_filtrado[df_filtrado['STATUS'].isin(st.session_state.status)]
    if 'faixa_tamanho' in st.session_state:
        min_t, max_t = st.session_state['faixa_tamanho']
        df = df[df['DESCRICAO'].str.split().apply(len).between(min_t, max_t)]
    if "data_inicial" in st.session_state and "data_final" in st.session_state:
        df_filtrado = df_filtrado[
            (df_filtrado['TEMPO'].dt.date >= st.session_state.data_inicial) &
            (df_filtrado['TEMPO'].dt.date <= st.session_state.data_final)
        ]


    estado_counts = df_filtrado['UF'].value_counts()
    cidade_counts = df_filtrado['Cidade'].value_counts()

    estados_validos = estado_counts[estado_counts >= st.session_state.min_estado].index.tolist()
    cidades_validas = cidade_counts[cidade_counts >= st.session_state.min_cidade].index.tolist()

    df_filtrado = df_filtrado[
        (df_filtrado['UF'].isin(estados_validos)) &
        (df_filtrado['Cidade'].isin(cidades_validas))
    ]

    return df_filtrado
