import pandas as pd
import re
from transformers import pipeline


df = pd.read_csv("comentarios_pokemon_megas.csv")

def clean_text(text):
    text = str(text).lower()  # Converte para minúsculas
    text = re.sub(r'http\S+', '', text)  # Remove links
    text = re.sub(r'\[.*?\]', '', text)  # Remove texto em colchetes como [removido]
    text = re.sub(r'\W', ' ', text)  # Remove caracteres não-alfanuméricos
    text = re.sub(r'\s+', ' ', text).strip() # Remove espaços extras
    return text

# Aplica a limpeza na coluna dos comentários
df['comment_cleaned'] = df['comment_body'].apply(clean_text)
df.dropna(subset=['comment_cleaned'], inplace=True) # Remove linhas sem texto

sentiment_pipeline = pipeline("sentiment-analysis", model="cardiffnlp/twitter-roberta-base-sentiment-latest")


def get_sentiment(text):
    truncated_text = text[:512]
    try:
        result = sentiment_pipeline(truncated_text)[0]
        return result['label']
    except Exception as e:
        return "error"


print("Iniciando a análise de sentimento...")
# Aplica a função de sentimento diretamente no DataFrame completo
df['sentiment'] = df['comment_cleaned'].apply(get_sentiment) 


df.to_csv("sentimento_pokemon_resultados.csv", index=False) 

print("Análise concluída!")
print(df[['comment_body', 'sentiment']].head())