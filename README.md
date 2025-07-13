# 📊 Dashboard Reclame Aqui – MBA em Ciência de Dados

Este projeto tem como objetivo criar um dashboard interativo em Python com Streamlit utilizando dados de reclamações do site **Reclame Aqui**.

## 🎯 Objetivos do Painel

- Visualização temporal do número de reclamações
- Frequência por estado
- Frequência por tipo de status
- Distribuição do tamanho das descrições
- WordCloud com palavras mais frequentes
- Mapa interativo com heatmap das reclamações por ano e estado

## 📁 Estrutura

```
reclame_aqui_dashboard/
│
├── data/              → Arquivo de dados CSV
├── notebooks/         → EDA e análise preliminar
├── app/               → Código principal da aplicação Streamlit
├── assets/            → Arquivos estáticos (ex: logo, imagens)
├── requirements.txt   → Bibliotecas necessárias
├── README.md          → Este arquivo
└── setup.sh           → Script para configurar o ambiente (opcional)
```

## ▶️ Como rodar o projeto

1. Clone o repositório:

```bash
git clone https://github.com/julianogueira3/dashboard-pdc.git
cd dashboard-pdc
```

2. Crie o ambiente virtual:

```bash
python -m venv .venv
source .venv/bin/activate     # Linux/macOS
.venv\Scripts\activate        # Windows
```

3. Instale as dependências:

```bash
pip install -r requirements.txt
```

4. Rode o app Streamlit:

```bash
streamlit run app/main.py
```

## 🚀 Deploy

Para fazer o deploy, recomendamos a plataforma **Streamlit Cloud**:
- https://streamlit.io/cloud

## 👥 Integrantes

- Julia Nunes – Matrícula: 2427399
- Ismael Góes – Matrícula: 2428140
- Jarlan Silva – Matrícula: 2427608 
- Artur Rodrigues Bastos - Matrícula: 2427753

## 🎥 Apresentação

📽️ Link do vídeo explicativo: https://drive.google.com/file/d/1zLkgwsgsQMs1K6RE343ks_X9fueLqRoq/view?usp=sharing

## 🌐 Aplicação hospedada

🔗 Link da aplicação: https://dashboard-pdc-bnpqdkbaa8hjhrt2rxtvms.streamlit.app
