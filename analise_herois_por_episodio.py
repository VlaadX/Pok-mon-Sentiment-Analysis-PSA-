
import pandas as pd
import re

print("Iniciando a análise de heróis por episódio...")


heroi_list = [
    "Hero X", "Queen", "Dragon Boy", "Ghostblade", "The Johnnies",
    "Little Johnny", "Big Johnny", "Loli", "Lucky Cyan", "Ahu",
    "E-Soul", "Nice", "Firm Man", "Lin ling"
]

heroi_list = sorted(list(set(heroi_list)))


input_filename = "comentarios_episodios_tobehero.csv"

try:
    df = pd.read_csv(input_filename)
    print(f"Arquivo '{input_filename}' carregado com {len(df)} comentários.")
except FileNotFoundError:
    print(f"ERRO: Arquivo '{input_filename}' não encontrado.")
    print("Por favor, execute o script 'coletor_episodios.py' primeiro.")
    exit()


df['comment_body'] = df['comment_body'].astype(str)


episodes = sorted(df['episode_number'].unique())
print(f"Episódios encontrados no arquivo: {episodes}")

results = []


for episode in episodes:

    episode_df = df[df['episode_number'] == episode]
    

    hero_mention_counts = {}
    

    for heroi in heroi_list:

        mentions = episode_df['comment_body'].str.contains(
            r'\b' + re.escape(heroi) + r'\b',
            case=False, 
            regex=True
        ).sum()
        
        hero_mention_counts[heroi] = mentions


    if sum(hero_mention_counts.values()) > 0:

        most_mentioned_hero = max(hero_mention_counts, key=hero_mention_counts.get)
        max_mentions = hero_mention_counts[most_mentioned_hero]
    else:
        most_mentioned_hero = "Nenhuma menção encontrada"
        max_mentions = 0
        
    print(f"Episódio {episode}: Herói em destaque é '{most_mentioned_hero}' com {max_mentions} menções.")
    

    results.append({
        'Episódio': episode,
        'Herói em Destaque': most_mentioned_hero,
        'Nº de Menções': max_mentions
    })


results_df = pd.DataFrame(results)


output_filename_summary = "heroi_destaque_por_episodio.csv"
results_df.to_csv(output_filename_summary, index=False)

print(f"\nAnálise concluída! Os resultados foram salvos em '{output_filename_summary}'.")
print("\nResumo do Resultado:")
print(results_df.to_string(index=False))