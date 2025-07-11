import streamlit as st
import plotly.express as px

def tab_status(df, container):
    with container:
        st.header("📦 Status das Reclamações")
        status_counts = df['STATUS'].value_counts()
        if not status_counts.empty:
            fig_status = px.bar(
                status_counts,
                x=status_counts.index,
                y=status_counts.values,
                color=status_counts.values,
                color_continuous_scale="Blues",
                labels={"x": "Status", "y": "Quantidade"},
                text=status_counts.values
            )
            fig_status.update_traces(textposition="outside")
            fig_status.update_layout(xaxis_tickangle=-45, coloraxis_showscale=False)
            st.plotly_chart(fig_status, use_container_width=True)
        else:
            st.info("Sem dados de status para exibir.")

        st.markdown("---")

        st.subheader("Status das Reclamações por Estado")
        if not df.empty:
            status_estado = df.groupby(['UF', 'STATUS']).size().reset_index(name='Qtd')
            fig_stack = px.bar(
                status_estado,
                x='UF',
                y='Qtd',
                color='STATUS',
                barmode='stack',
                color_discrete_sequence=px.colors.qualitative.Set3,
                labels={"Qtd": "Quantidade"}
            )
            fig_stack.update_layout(xaxis_tickangle=-45)
            st.plotly_chart(fig_stack, use_container_width=True)
        else:
            st.info("Sem dados para o gráfico Status por Estado.")
