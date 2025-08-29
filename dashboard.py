
import streamlit as st
import pandas as pd
import plotly.express as px

# --- CONFIGURAÇÃO DA PÁGINA ---

st.set_page_config(
    page_title="Análise de Sentimento Pokémon",
    page_icon="🐉",
    layout="wide"  
)

# --- FUNÇÃO DE CARREGAMENTO DE DADOS ---
@st.cache_data 
def load_data():
    try:
        df = pd.read_csv("sentimento_pokemon_resultados.csv")

        sentiment_map = {'positive': 'Positivo', 'neutral': 'Neutro', 'negative': 'Negativo'}
        df['sentiment_label'] = df['sentiment'].map(sentiment_map)
        return df
    except FileNotFoundError:
        st.error("Arquivo 'sentimento_pokemon_resultados.csv' não encontrado. Execute o 'analisador_sentimento.py' primeiro.")
        return None

df = load_data()

# --- BARRA LATERAL (SIDEBAR) PARA FILTROS ---

st.sidebar.header("Filtros da Análise")


pokemon_list = ["Dragonite", "Victreebell", "Hawlucha"]

selected_pokemon = st.sidebar.multiselect(
    "Escolha os Pokémon para Análise Detalhada:",
    options=pokemon_list,
    default=["Dragonite", "Victreebell", "Hawlucha"]
)

--
st.title("📊 Análise de Sentimento: Megaevoluções Especuladas")
st.markdown("Recepção da comunidade do Reddit sobre *Pokémon Legends: Z-A*.")

if df is None:
    st.stop()

# --- SEÇÃO 1: MÉTRICAS CHAVE (KPIs) ---

col1, col2, col3 = st.columns(3)
total_comentarios = len(df)
comentarios_positivos = len(df[df['sentiment_label'] == 'Positivo'])
porcentagem_positiva = (comentarios_positivos / total_comentarios) * 100 if total_comentarios > 0 else 0

col1.metric("Total de Comentários Analisados", f"{total_comentarios:,}")
col2.metric("Comentários Positivos", f"{comentarios_positivos:,}")
col3.metric("Taxa de Aprovação Geral", f"{porcentagem_positiva:.1f}%")

st.markdown("---") 

# --- SEÇÃO 2: GRÁFICOS ---
col_pie, col_bar = st.columns(2) 


sentiment_colors = {'Positivo': '#28a745', 'Neutro': '#ffc107', 'Negativo': '#dc3545'}


with col_pie:
    st.subheader("Distribuição Geral de Sentimentos")
    sentiment_counts = df['sentiment_label'].value_counts()
    fig_pie = px.pie(
        sentiment_counts,
        values=sentiment_counts.values,
        names=sentiment_counts.index,
        hole=0.4, 
        color=sentiment_counts.index,
        color_discrete_map=sentiment_colors
    )
    fig_pie.update_traces(textposition='inside', textinfo='percent+label', hoverinfo='label+percent+value')
    fig_pie.update_layout(showlegend=False, margin=dict(t=20, b=20, l=20, r=20))
    st.plotly_chart(fig_pie, use_container_width=True)


with col_bar:
    st.subheader("Análise Detalhada por Pokémon")
    if selected_pokemon:
        comparison_data = []
        df['comment_body'] = df['comment_body'].astype(str)

        for pokemon in selected_pokemon:
            pokemon_df = df[df['comment_body'].str.contains(pokemon, case=False)]
            if not pokemon_df.empty:
                counts = pokemon_df['sentiment_label'].value_counts().reindex(['Positivo', 'Neutro', 'Negativo'], fill_value=0)
                for sentiment, count in counts.items():
                    comparison_data.append([pokemon, sentiment, count])

        if comparison_data:
            comparison_df = pd.DataFrame(comparison_data, columns=['Pokémon', 'Sentimento', 'Contagem'])
            fig_bar = px.bar(
                comparison_df,
                x='Pokémon',
                y='Contagem',
                color='Sentimento',
                barmode='group',
                color_discrete_map=sentiment_colors,
                text_auto=True, # Adiciona os valores nas barras
                labels={'Contagem':'Contagem de Comentários'}
            )

            fig_bar.update_layout(
                plot_bgcolor='rgba(0,0,0,0)', 
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(family="Arial, sans-serif", size=12, color="black"),
                title=None, 
                xaxis_title=None,
                yaxis_title="Contagem de Comentários",
                legend_title_text=None,
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                margin=dict(t=20, b=0, l=0, r=0)
            )
            fig_bar.update_xaxes(showgrid=False)
            fig_bar.update_yaxes(showgrid=True, gridcolor='#e5e5e5')
            fig_bar.update_traces(textposition='outside', textfont_size=12)
            st.plotly_chart(fig_bar, use_container_width=True)
        else:
            st.warning("Nenhum comentário encontrado para os Pokémon selecionados.")
    else:
        st.info("Selecione um Pokémon na barra lateral para ver a análise detalhada.")

# --- SEÇÃO 3: DADOS BRUTOS ---

with st.expander("Visualizar Tabela de Dados Brutos"):
    st.dataframe(df)