import pandas as pd
import re
from transformers import pipeline

try:
    df = pd.read_csv("comentarios_tobehero_v3.csv")
    print("Arquivo 'comentarios_tobehero.csv' carregado com sucesso.")
except FileNotFoundError:
    print("Erro: Arquivo 'comentarios_tobehero.csv' não encontrado.")

    df = pd.DataFrame({
        'comment_body': [
            "This is absolutely fantastic! Love the new features :)",
            "I'm not sure how I feel about this update.",
            "This is the worst change you have ever made. Awful!!!",
            "it's ok i guess",
            "Check out my profile http://example.com"
        ]
    })
    print("Usando um DataFrame de exemplo para demonstração.")


def clean_text(text):
    text = str(text)

    text = re.sub(r'http\S+', '', text)

    text = re.sub(r'\s+', ' ', text).strip()
    return text


df['comment_cleaned'] = df['comment_body'].apply(clean_text)
df.dropna(subset=['comment_cleaned'], inplace=True)

df = df[df['comment_cleaned'] != '']

print("\nCarregando o modelo de análise de sentimento (pode levar um momento)...")
sentiment_pipeline = pipeline(
    "sentiment-analysis",
    model="cardiffnlp/twitter-roberta-base-sentiment-latest"
)
print("Modelo carregado com sucesso!")



def get_sentiment(text):

    truncated_text = text[:512]
    try:

        result = sentiment_pipeline(truncated_text)[0]

        return result['label'].upper()
    except Exception as e:
        print(f"Não foi possível analisar o texto: '{truncated_text[:50]}...'. Erro: {e}")
        return "ERROR"



print("\nIniciando a análise de sentimento em todos os comentários...")

df['sentiment'] = df['comment_cleaned'].apply(get_sentiment)
print("Análise concluída!")



output_filename = "sentimento_tobehero_heroi_resultados_final.csv"
df.to_csv(output_filename, index=False)
print(f"\nResultados salvos com sucesso em '{output_filename}'")



print("\nAmostra dos resultados:")

print(df[['comment_body', 'sentiment']].head())

