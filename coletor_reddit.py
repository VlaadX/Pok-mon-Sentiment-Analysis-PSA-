import praw
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()

# --- CONFIGURAÇÃO DE CREDENCIAIS ---
reddit = praw.Reddit(
    client_id=os.getenv("REDDIT_CLIENT_ID"),
    client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
    user_agent=f"HeroSentimentAnalyzer by u/{os.getenv('REDDIT_USERNAME')}",
    username=os.getenv("REDDIT_USERNAME"),
    password=os.getenv("REDDIT_PASSWORD")
)

subreddits = ["ToBeHero_X"]
keywords = [
    "Firm Man",
    "Queen",
    "Dragon Boy",
    "Ghostblade",
    "The Johnnies",
    "Little Johnny",
    "Big Johnny",
    "Loli",
    "Lucky Cyan",
    "Ahu",
    "E-Soul",
    "Nice"
]

all_comments = []

processed_comment_ids = set()


keywords_lower = [k.lower() for k in keywords]

print("Iniciando a busca por posts e comentários relevantes...")
for sub in subreddits:
    subreddit = reddit.subreddit(sub)
    for keyword in keywords:
        print(f"Buscando posts com a palavra-chave: '{keyword}' no subreddit r/{sub}...")

        for submission in subreddit.search(keyword, limit=25):

            submission.comments.replace_more(limit=0)

            for comment in submission.comments.list():

                if not comment.body or comment.body == '[removed]' or comment.body == '[deleted]' or comment.id in processed_comment_ids:
                    continue

                comment_body_lower = comment.body.lower()
                

                if any(hero in comment_body_lower for hero in keywords_lower):
                    all_comments.append({
                        'subreddit': sub,
                        'post_title': submission.title,
                        'comment_body': comment.body,
                        'score': comment.score
                    })

                    processed_comment_ids.add(comment.id)


print(f"\nColetados {len(all_comments)} comentários relevantes.")


df = pd.DataFrame(all_comments)


output_filename = "comentarios_tobehero_v3.csv"
df.to_csv(output_filename, index=False)


print(f"Dados salvos em {output_filename}")