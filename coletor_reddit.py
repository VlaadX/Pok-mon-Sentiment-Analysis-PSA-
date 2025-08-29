import praw
import pandas as pd


# --- CONFIGURAÇÃO DE CREDENCIAIS  ---
reddit = praw.Reddit(
    client_id=os.getenv("REDDIT_CLIENT_ID"),
    client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
    user_agent=f"PokemonSentimentAnalyzer by u/{os.getenv('REDDIT_USERNAME')}",
    username=os.getenv("REDDIT_USERNAME"),
    password=os.getenv("REDDIT_PASSWORD")
)

subreddits = ["pokemon", "pokeleaks", "PokemonLegendsZA"]
keywords = ["mega evolucao","Mega Dragonite","Mega Victreebell", "Mega Hawlucha"] 

all_comments = []

print("Iniciando a busca por posts...")
for sub in subreddits:
    subreddit = reddit.subreddit(sub)
    for keyword in keywords:
        # Busca por posts (submissions) que contenham a palavra-chave
        for submission in subreddit.search(keyword, limit=25):
            submission.comments.replace_more(limit=0) 
            for comment in submission.comments.list():
                all_comments.append({
                    'subreddit': sub,
                    'post_title': submission.title,
                    'comment_body': comment.body,
                    'score': comment.score
                })

print(f"Coletados {len(all_comments)} comentários.")


df = pd.DataFrame(all_comments)
df.to_csv("comentarios_pokemon_megas.csv", index=False)

print("Dados salvos em comentarios_pokemon.csv")