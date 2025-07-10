import streamlit as st
from wordcloud import WordCloud
import matplotlib.pyplot as plt

def tab_nuvem(df, container):
    with container:
        st.header("Nuvem de Palavras das Reclamações")

        if 'DESCRICAO' not in df.columns:
            st.warning("A coluna 'DESCRICAO' não está presente no dataframe.")
            return

        texto = " ".join(df['DESCRICAO'].dropna().astype(str))

        if not texto.strip():
            st.warning("Nenhum texto disponível para gerar a nuvem de palavras.")
            return

        wordcloud = WordCloud(
            width=800,
            height=400,
            background_color='white',
            max_words=200,
            collocations=False
        ).generate(texto)

        fig, ax = plt.subplots(figsize=(10, 5))
        ax.imshow(wordcloud, interpolation='bilinear')
        ax.axis("off")
        st.pyplot(fig)