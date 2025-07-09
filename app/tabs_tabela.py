import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode

def tab_tabela(df, container):
    with container:
        st.header("Tabela de Reclamações Filtrada")
        colunas_exibidas = ["ID", "TEMA", "LOCAL", "TEMPO", "CATEGORIA", "STATUS", "DESCRICAO"]

        if not df.empty:
            df_tabela = df[colunas_exibidas].copy()
            gb = GridOptionsBuilder.from_dataframe(df_tabela)
            gb.configure_default_column(filter=True, sortable=True, editable=False, resizable=True)
            gb.configure_selection(selection_mode="single", use_checkbox=True)
            grid_options = gb.build()

            grid_response = AgGrid(
                df_tabela,
                gridOptions=grid_options,
                update_mode=GridUpdateMode.SELECTION_CHANGED,
                theme='material',
                height=400,
                fit_columns_on_grid_load=True,
                enable_enterprise_modules=False,
            )
            selected = grid_response['selected_rows']
            if selected:
                st.markdown("### Reclamação Selecionada")
                st.write(selected[0])
        else:
            st.info("Nenhum dado encontrado para os filtros selecionados.")
