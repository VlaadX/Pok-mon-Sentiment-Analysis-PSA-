import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Análise por Episódio", layout="wide")

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

df_episodios = load_data("sentimento_episodios_final.csv")
df_destaques = load_data("heroi_destaque_por_episodio.csv")
sentiment_colors = {'Positivo': '#28a745', 'Neutro': '#ffc107', 'Negativo': '#dc3545'}


st.title("Análise de Sentimento por Episódio")
st.markdown("Acompanhe a evolução da recepção da comunidade ao longo da temporada.")

if df_episodios is None or df_destaques is None:
    st.error("Arquivos 'sentimento_episodios_final.csv' ou 'heroi_destaque_por_episodio.csv' não encontrados!")
    st.stop()

# --- SEÇÃO 1: DESTAQUES POR EPISÓDIO ---
st.subheader("Herói Mais Comentado a Cada Episódio")
st.dataframe(df_destaques, use_container_width=True)

st.markdown("---")

# --- SEÇÃO 2: EVOLUÇÃO DO SENTIMENTO ---
st.subheader("Evolução do Sentimento ao Longo dos Episódios")

# Calcula a porcentagem de cada sentimento por episódio
sentiment_over_time = df_episodios.groupby(['episode_number', 'sentiment_label']).size().unstack(fill_value=0)
sentiment_percentage = sentiment_over_time.apply(lambda x: x / x.sum() * 100, axis=1).reset_index()
sentiment_percentage_melted = sentiment_percentage.melt(
    id_vars='episode_number', value_vars=['Positivo', 'Neutro', 'Negativo'],
    var_name='Sentimento', value_name='Porcentagem'
)

fig_line = px.line(
    sentiment_percentage_melted,
    x='episode_number', y='Porcentagem', color='Sentimento',
    labels={'episode_number': 'Episódio', 'Porcentagem': 'Porcentagem de Comentários (%)'},
    color_discrete_map=sentiment_colors, markers=True
)
fig_line.update_layout(
    yaxis_ticksuffix="%", legend_title_text=None,
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
)
st.plotly_chart(fig_line, use_container_width=True)

# --- SEÇÃO 3: EXPLORE UM EPISÓDIO ---
st.markdown("---")
st.subheader("Análise de um Episódio Específico")
episode_list = sorted(df_episodios['episode_number'].unique())
selected_episode = st.selectbox("Selecione um episódio para ver detalhes:", options=episode_list)

if selected_episode:
    df_ep_filtrado = df_episodios[df_episodios['episode_number'] == selected_episode]
    st.dataframe(df_ep_filtrado[['comment_body', 'sentiment_label']].rename(columns={'comment_body': 'Comentário', 'sentiment_label': 'Sentimento'}), height=400)