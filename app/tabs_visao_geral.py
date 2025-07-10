import streamlit as st
import plotly.express as px

def tab_visao_geral(df, container):
    with container:
        st.header("Visão Geral")

        # Select para top_n aqui, antes dos gráficos
        top_options = [5, 10, 15, 20, "Todos"]
        top_n = st.selectbox(
            "Quantidade de Top para gráficos", 
            options=top_options, 
            index=top_options.index(st.session_state.get("top_n", 5)) if st.session_state.get("top_n") in top_options else 0,
            key="top_n"
        )

        top_n_int = 999999 if top_n == "Todos" else top_n

        col1, col2, col3 = st.columns(3)
        col1.metric("Cidades únicas", df['Cidade'].nunique())
        col2.metric("Estados únicos", df['UF'].nunique())
        col3.metric("Total Reclamações", len(df))

        st.markdown("---")
        col4, col5 = st.columns(2)

        with col4:
            st.subheader(f"Top {top_n_int} Cidades com Mais Reclamações")
            cidade_counts = df['Cidade'].value_counts().head(top_n_int)
            if not cidade_counts.empty:
                fig_cid = px.bar(
                    cidade_counts,
                    x=cidade_counts.index,
                    y=cidade_counts.values,
                    labels={"x": "Cidade", "y": "Quantidade"},
                    color=cidade_counts.values,
                    color_continuous_scale="Blues",
                    text=cidade_counts.values
                )
                fig_cid.update_traces(textposition="outside")
                fig_cid.update_layout(yaxis_title="Reclamações", xaxis_tickangle=-45, coloraxis_showscale=False)
                st.plotly_chart(fig_cid, use_container_width=True)
            else:
                st.info("Sem dados de cidades para exibir.")

        with col5:
            st.subheader(f"Top {top_n_int} Estados com Mais Reclamações")
            estado_counts = df['UF'].value_counts().head(top_n_int)
            if not estado_counts.empty:
                fig_est = px.bar(
                    estado_counts,
                    x=estado_counts.index,
                    y=estado_counts.values,
                    labels={"x": "Estado", "y": "Quantidade"},
                    color=estado_counts.values,
                    color_continuous_scale="Blues",
                    text=estado_counts.values
                )
                fig_est.update_traces(textposition="outside")
                fig_est.update_layout(yaxis_title="Reclamações", xaxis_tickangle=-45, coloraxis_showscale=False)
                st.plotly_chart(fig_est, use_container_width=True)
            else:
                st.info("Sem dados de estados para exibir.")
