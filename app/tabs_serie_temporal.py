import streamlit as st
import plotly.express as px
import pandas as pd

def tab_serie_temp(df, container):
    # Garantir que a coluna TEMPO esteja no formato datetime
    df['TEMPO'] = pd.to_datetime(df['TEMPO'])

    # Criar uma nova coluna com o mês e o ano (ex: '2025-07')
    df['MES_ANO'] = df['TEMPO'].dt.to_period('M').astype(str)

    # Contar quantos casos houve por mês
    status_counts = df['MES_ANO'].value_counts().sort_index()

    with container:
        st.header("📅 Reclamações por Mês")
        if not status_counts.empty:
            fig_status = px.bar(
                status_counts,
                x=status_counts.index,
                y=status_counts.values,
                color=status_counts.values,
                color_continuous_scale="Blues",
                labels={"x": "Mês/Ano", "y": "Quantidade"},
                text=status_counts.values
            )
            fig_status.update_traces(textposition="outside",
                                     hovertemplate='<b>Mês/Ano:</b> %{x}<br><b>Quantidade:</b> %{y}<extra></extra>')
            fig_status.update_layout(xaxis_tickangle=-45, coloraxis_showscale=False)
            st.plotly_chart(fig_status, use_container_width=True)
        else:
            st.info("Sem dados de tempo para exibir.")