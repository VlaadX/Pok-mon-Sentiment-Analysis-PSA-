import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Análise de Sentimento | To Be Hero",
    page_icon="🦸",
    layout="wide"
)


@st.cache_data
def load_data(file_path):
    try:
        return pd.read_csv(file_path)
    except FileNotFoundError:
        return None


df_herois = load_data("sentimento_herois_final.csv")
df_episodios = load_data("sentimento_episodios_final.csv")

# --- PÁGINA PRINCIPAL ---
st.title("📊 Dashboard de Análise de Sentimento da Comunidade 'To Be Hero'")
st.markdown("""
Bem-vindo à análise de sentimento sobre o anime **To Be Hero X**. Este dashboard explora a recepção da comunidade do Reddit, 
analisando milhares de comentários para entender as opiniões sobre os **personagens** e a **evolução da série, episódio por episódio**.

**Use o menu na barra lateral à esquerda para navegar entre as análises detalhadas.**
""")

st.markdown("---")

# --- MÉTRICAS GERAIS DO PROJETO ---
st.header("Números Gerais do Projeto")

if df_herois is not None and df_episodios is not None:
    total_comentarios_herois = len(df_herois)
    total_comentarios_episodios = len(df_episodios)
    total_comentarios = total_comentarios_herois + total_comentarios_episodios
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Total de Comentários Analisados", f"{total_comentarios:,}")
    col2.metric("Comentários sobre Heróis", f"{total_comentarios_herois:,}")
    col3.metric("Comentários sobre Episódios", f"{total_comentarios_episodios:,}")
else:
    st.error("Um ou mais arquivos CSV não foram encontrados. Por favor, verifique os nomes e a localização dos arquivos.")

st.markdown("<br><br>", unsafe_allow_html=True)
st.info("Este projeto utiliza Processamento de Linguagem Natural (NLP) para classificar os comentários e extrair insights sobre a opinião pública da fanbase.", icon="💡")