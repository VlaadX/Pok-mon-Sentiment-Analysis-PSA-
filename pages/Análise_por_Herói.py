import streamlit as st
import pandas as pd
import plotly.express as px
import re

st.set_page_config(page_title="Análise por Herói", layout="wide")

# --- FUNÇÕES E CONFIGURAÇÕES ---
@st.cache_data
def load_data(file_path):
    try:
        df = pd.read_csv(file_path)

        if 'sentiment' in df.columns:
            sentiment_map = {'POSITIVE': 'Positivo', 'NEUTRAL': 'Neutro', 'NEGATIVE': 'Negativo'}
            df['sentiment_label'] = df['sentiment'].str.upper().map(sentiment_map)
            df.dropna(subset=['sentiment_label'], inplace=True)
        return df
    except FileNotFoundError:
        return None

df_herois = load_data("sentimento_herois_final.csv")
sentiment_colors = {'Positivo': '#28a745', 'Neutro': '#ffc107', 'Negativo': '#dc3545'}

# --- LAYOUT DA PÁGINA ---
st.title("Análise de Sentimento por Herói")
st.markdown("Explore a recepção de cada personagem com base nos comentários da comunidade.")

if df_herois is None:
    st.error("Arquivo 'sentimento_herois_final.csv' não encontrado!")
    st.stop()

# --- GRÁFICO PRINCIPAL ---
st.subheader("Comparativo de Sentimentos por Herói")

heroi_list = sorted(list(set(re.findall(r'\b[A-Z][a-z]+(?: [A-Z][a-z]+)?\b', ' '.join(df_herois['comment_body'].astype(str).unique()))))) # Tenta extrair nomes

heroi_list = sorted(["Queen", "Dragon Boy", "Ghostblade", "Little Johnny", "Big Johnny", "Loli", "Lucky Cyan", "Ahu", "E-Soul", "Nice", "Firm Man", "Lin ling"])

comparison_data = []
for heroi in heroi_list:
    heroi_df = df_herois[df_herois['comment_body'].astype(str).str.contains(r'\b' + re.escape(heroi) + r'\b', case=False, regex=True)]
    if not heroi_df.empty:
        counts = heroi_df['sentiment_label'].value_counts().reindex(['Positivo', 'Neutro', 'Negativo'], fill_value=0)
        for sentiment, count in counts.items():
            comparison_data.append([heroi, sentiment, count])

if comparison_data:
    comparison_df = pd.DataFrame(comparison_data, columns=['Herói', 'Sentimento', 'Contagem'])
    fig_bar = px.bar(
        comparison_df, x='Herói', y='Contagem', color='Sentimento', barmode='group',
        color_discrete_map=sentiment_colors, text_auto=True, labels={'Contagem':'Nº de Comentários'}
    )
    fig_bar.update_layout(
        yaxis_title="Nº de Comentários", xaxis_title=None,
        legend_title_text=None, legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    st.plotly_chart(fig_bar, use_container_width=True)

# --- VISUALIZAÇÃO DE DADOS BRUTOS ---
st.markdown("---")
st.subheader("Explore os Comentários")
selected_heroi_filter = st.selectbox("Filtre comentários por um herói específico:", options=["Todos"] + heroi_list)

if selected_heroi_filter != "Todos":
    df_display = df_herois[df_herois['comment_body'].astype(str).str.contains(r'\b' + re.escape(selected_heroi_filter) + r'\b', case=False, regex=True)]
else:
    df_display = df_herois

st.dataframe(df_display[['comment_body', 'sentiment_label']].rename(columns={'comment_body': 'Comentário', 'sentiment_label': 'Sentimento'}), height=400)