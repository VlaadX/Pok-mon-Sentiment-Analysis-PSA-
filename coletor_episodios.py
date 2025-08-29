# Nome do arquivo: coletor_episodios.py

import praw
import pandas as pd
import os
from dotenv import load_dotenv
import re

load_dotenv()

# --- CONFIGURAÇÃO DE CREDENCIAIS ---
reddit = praw.Reddit(
    client_id=os.getenv("REDDIT_CLIENT_ID"),
    client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
    user_agent=f"HeroEpisodeAnalyzer by u/{os.getenv('REDDIT_USERNAME')}",
    username=os.getenv("REDDIT_USERNAME"),
    password=os.getenv("REDDIT_PASSWORD")
)

subreddits = ["ToBeHero_X"]
total_episodes = 20 

all_comments = []
processed_comment_ids = set()

print("Iniciando a busca por posts de discussão de episódios...")

for sub in subreddits:
    subreddit = reddit.subreddit(sub)
    

    for i in range(1, total_episodes + 1):

        search_queries = [
            f"Episode {i} Discussion",
            f"Ep {i} Discussion",
            f"Episode {i}",
        ]
        
        print(f"\nBuscando posts para o Episódio {i} em r/{sub}...")
        
        found_episode_posts = False
        for query in search_queries:

            for submission in subreddit.search(query, limit=5, sort="relevance"):

                if str(i) in submission.title:
                    found_episode_posts = True
                    print(f"  -> Encontrado post relevante: '{submission.title[:60]}...'")
                    
                    submission.comments.replace_more(limit=0)
                    for comment in submission.comments.list():

                        if not comment.body or comment.body in ['[removed]', '[deleted]'] or comment.id in processed_comment_ids:
                            continue
                        

                        all_comments.append({
                            'episode_number': i,
                            'subreddit': sub,
                            'post_title': submission.title,
                            'comment_body': comment.body,
                            'score': comment.score
                        })
                        processed_comment_ids.add(comment.id)
        
        if not found_episode_posts:
            print(f"  -> Nenhum post de discussão encontrado para o Episódio {i}.")


print(f"\n\nColetados {len(all_comments)} comentários de discussões de episódios.")


df = pd.DataFrame(all_comments)


output_filename = "comentarios_episodios_tobehero.csv"
df.to_csv(output_filename, index=False)

print(f"Dados salvos em {output_filename}")