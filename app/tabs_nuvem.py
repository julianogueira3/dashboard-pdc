import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from wordcloud import WordCloud
import nltk
from nltk.corpus import stopwords

nltk.download('stopwords', quiet=True)

def count_palavras(texto):
    return len(texto.split())

def tab_nuvem(df, container):
    with container:
        st.header("🧠 Análise de Texto e Categorias de Reclamações")

        if 'DESCRICAO' not in df.columns or 'TEMA' not in df.columns or 'CATEGORIA' not in df.columns:
            st.warning("As colunas 'DESCRICAO', 'TEMA' ou 'CATEGORIA' estão ausentes.")
            return

        stopwords_portugues = stopwords.words('portuguese')
        novas_stopwords = [
            "porém", "nada", "fiz", "sendo", "outro", "Reclame", "Aqui", "Quero", "ainda", "pois", "ter", "pra", "todo",
            "nao", "porque", "Editado", "outra", "assim",
            "Pão", "Açúcar", "Açucar", "mercado", "supermercado", "unidade",
            "entrei", "fazer", "sobre", "todos", "data", "bem", "havia", "lá"
        ]
        stopwords_personalizadas = set(stopwords_portugues + novas_stopwords)

        texto_desc = " ".join(df['DESCRICAO'].dropna().astype(str))
        texto_tema = " ".join(df['TEMA'].dropna().astype(str))

        # Selectbox para escolher o grupo de gráficos
        opcao = st.selectbox("Selecione o grupo de gráficos para visualizar:", 
                             ["Distribuição de Palavras", "Nuvens de Palavras", "Frequência de Categorias", "Frequência por Estado"])

        if opcao == "Distribuição de Palavras":
            palavras = df['DESCRICAO'].dropna().astype(str).apply(count_palavras)
            col1, col2 = st.columns(2)

            with col1:
                fig, ax = plt.subplots(figsize=(6, 4))
                sns.histplot(palavras, kde=False, stat='density', ax=ax, color='skyblue')
                ax.set_title('Histograma da Quantidade de Palavras')
                st.pyplot(fig)

            with col2:
                fig2, ax2 = plt.subplots(figsize=(6, 4))
                sns.kdeplot(palavras, ax=ax2, fill=True, color='purple')
                ax2.set_title('Densidade KDE da Quantidade de Palavras')
                st.pyplot(fig2)

        elif opcao == "Nuvens de Palavras":
            col1, col2 = st.columns(2)

            with col1:
                st.markdown("**🔤 Nuvem de Palavras – DESCRIÇÃO**")
                if texto_desc.strip():
                    max_words_desc = st.slider("Máximo de palavras para Nuvem DESCRIÇÃO", 10, 200, 50, key="max_words_desc")
                    wordcloud_desc = WordCloud(
                        width=600, height=300, background_color='white',
                        stopwords=stopwords_personalizadas,
                        colormap='viridis', max_words=max_words_desc
                    ).generate(texto_desc)
                    fig, ax = plt.subplots(figsize=(6, 3))
                    ax.imshow(wordcloud_desc, interpolation='bilinear')
                    ax.axis('off')
                    st.pyplot(fig)
                else:
                    st.warning("Sem conteúdo em DESCRICAO")

            with col2:
                st.markdown("**📝 Nuvem de Palavras – TEMA**")
                if texto_tema.strip():
                    max_words_tema = st.slider("Máximo de palavras para Nuvem TEMA", 10, 200, 50, key="max_words_tema")
                    wordcloud_tema = WordCloud(
                        width=600, height=300, background_color='white',
                        stopwords=stopwords_personalizadas,
                        colormap='viridis', max_words=max_words_tema
                    ).generate(texto_tema)
                    fig, ax = plt.subplots(figsize=(6, 3))
                    ax.imshow(wordcloud_tema, interpolation='bilinear')
                    ax.axis('off')
                    st.pyplot(fig)
                else:
                    st.warning("Sem conteúdo em TEMA")

        elif opcao == "Frequência de Categorias":
            df_explodido = df.assign(CATEGORIA_separada=df['CATEGORIA'].str.split('<->')).explode('CATEGORIA_separada')
            indesejadas = ['Supermercados', 'Pão de Açúcar', 'Não encontrei meu problema', 'Hipermercados']
            df_filtrado = df_explodido[~df_explodido['CATEGORIA_separada'].isin(indesejadas)]

            freq_df = df_filtrado['CATEGORIA_separada'].value_counts().reset_index()
            freq_df.columns = ['Categoria', 'Frequência']

            freq_min = st.slider("Frequência mínima para categorias exibidas", 1, 100, 10, key="freq_min_cat")
            freq_df_filtrado = freq_df[freq_df['Frequência'] > freq_min]

            if not freq_df_filtrado.empty:
                fig, ax = plt.subplots(figsize=(10, 6))
                sns.barplot(data=freq_df_filtrado, y='Categoria', x='Frequência', palette='viridis', ax=ax)
                ax.set_title(f'Categorias mais frequentes (> {freq_min})')
                st.pyplot(fig)
            else:
                st.info("Nenhuma categoria com frequência maior que o mínimo selecionado.")

        elif opcao == "Frequência por Estado":
            df_explodido = df.assign(CATEGORIA_separada=df['CATEGORIA'].str.split('<->')).explode('CATEGORIA_separada')
            indesejadas = ['Supermercados', 'Pão de Açúcar', 'Não encontrei meu problema', 'Hipermercados']
            df_filtrado = df_explodido[~df_explodido['CATEGORIA_separada'].isin(indesejadas)]

            freq_total = df_filtrado.groupby('CATEGORIA_separada').size().reset_index(name='Total')
            categorias_validas = freq_total[freq_total['Total'] > 10]['CATEGORIA_separada']

            freq_uf = df_filtrado[df_filtrado['CATEGORIA_separada'].isin(categorias_validas)]
            freq_uf = freq_uf.groupby(['CATEGORIA_separada', 'UF']).size().reset_index(name='Frequência')

            ordem = freq_total.sort_values('Total', ascending=False)['CATEGORIA_separada'].tolist()

            if not freq_uf.empty:
                fig = px.bar(freq_uf,
                             x='CATEGORIA_separada',
                             y='Frequência',
                             color='UF',
                             category_orders={'CATEGORIA_separada': ordem},
                             title='Frequência de Categorias por Estado (UF)',
                             labels={'CATEGORIA_separada': 'Categoria', 'Frequência': 'Frequência', 'UF': 'Estado'},
                             height=500)
                fig.update_layout(barmode='stack', xaxis_tickangle=-45)
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Nenhum dado válido para UF")
