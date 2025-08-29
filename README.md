# 📊 Análise de Sentimento: Especulações de Megaevoluções Pokémon

A análise de sentimento, também conhecida como mineração de opinião, é uma técnica de Processamento de Linguagem Natural (PLN) usada para determinar o tom emocional expresso em um texto. O objetivo é entender se o texto transmite um sentimento positivo, negativo ou neutro.

No contexto da indústria de jogos e entretenimento, a análise de sentimento é crucial para:

* **Análise de Feedback da Comunidade:** Entender a recepção de novos anúncios, trailers ou vazamentos.
* **Monitoramento de Marca:** Acompanhar a percepção pública da franquia.
* **Pesquisa de Mercado:** Identificar quais características ou personagens são mais desejados pelos fãs.
* **Gerenciamento de Crises:** Detectar rapidamente focos de insatisfação na comunidade.

Neste projeto, queremos analisar o sentimento da comunidade de fãs de Pokémon em relação às especulações sobre as novas Megaevoluções para o aguardado jogo *Pokémon Legends: Z-A*. Os dados para análise foram coletados em tempo real de discussões na plataforma Reddit.

## 1.0 Problema de Negócio

Uma empresa de entretenimento como a The Pokémon Company está constantemente tomando decisões sobre o futuro de suas franquias, baseadas em parte na recepção e no desejo da sua base de fãs. Com o anúncio de *Pokémon Legends: Z-A* e o retorno das Megaevoluções, surge uma questão de negócio fundamental: **Quais das possíveis novas Megaevoluções estão gerando mais expectativa positiva e quais estão sendo recebidas com ceticismo ou desinteresse?**

Uma resposta baseada em dados a essa pergunta pode influenciar campanhas de marketing, design de produto e estratégias de comunicação. Utilizando métodos de PLN e web scraping, construí um modelo capaz de coletar e analisar milhares de comentários de fãs para quantificar o sentimento associado a cada Pokémon especulado. A solução final é um dashboard interativo construído com Streamlit para consulta rápida.

## 2.0 Fonte dos Dados

Os dados não vieram de um dataset estático, mas foram coletados diretamente da API do Reddit usando a biblioteca PRAW.

- **Fonte:** Comentários em posts de subreddits de Pokémon.
- **Subreddits Alvo:** `r/pokemon`, `r/pokeleaks`, `r/PokemonLegendsZA`.
- **Dados Coletados:** Corpo do comentário, título do post, subreddit de origem e pontuação do comentário.

## 3.0 Estratégia da Solução

O projeto foi estruturado em um pipeline claro, desde a coleta de dados brutos até a apresentação de insights em um dashboard interativo.

1.  **Coleta de Dados:** Um script Python (`coletor_reddit.py`) foi desenvolvido para se conectar à API do Reddit e buscar posts contendo palavras-chave específicas (ex: "Mega Dragonite", "legends z-a"). Todos os comentários desses posts foram extraídos e armazenados.
2.  **Pré-processamento e Limpeza:** Os textos dos comentários foram limpos para remover ruídos como links, pontuações e caracteres especiais, e padronizados para letras minúsculas.
3.  **Análise de Sentimento:** Foi utilizado um modelo de linguagem pré-treinado (`cardiffnlp/twitter-roberta-base-sentiment-latest`) da plataforma Hugging Face. Este modelo, baseado na arquitetura RoBERTa, é especializado em textos de redes sociais.
4.  **Agregação e Visualização:** Os resultados da análise foram agregados usando Pandas e visualizados com a biblioteca Plotly para criar gráficos interativos.
5.  **Dashboard Interativo:** Todos os componentes foram integrados em uma aplicação web (`dashboard.py`) com Streamlit, permitindo que um usuário final filtre e explore os dados de forma intuitiva.

## 4.0 Alguns Insights Visuais

O resultado final é o próprio dashboard, que consolida os insights. Os principais componentes visuais são:

**Distribuição Geral de Sentimentos:**
* Um gráfico de rosca (donut chart) mostra a proporção geral de comentários positivos, neutros e negativos.

**Comparação de Sentimento por Pokémon:**
* Um gráfico de barras agrupadas permite a comparação direta da recepção de cada Megaevolução especulada.

![Screenshot do Dashboard](https://github.com/VlaadX/Pok-mon-Sentiment-Analysis-PSA-/blob/main/imgs/dashboard.PNG)

## 5.0 Modelo de Análise de Sentimento

O coração da análise é o modelo **RoBERTa (Robustly optimized BERT approach)**, especificamente a versão `cardiffnlp/twitter-roberta-base-sentiment-latest`. Esta é uma implementação da arquitetura Transformer que foi pré-treinada em um volume massivo de texto e, em seguida, ajustada especificamente para a tarefa de classificar o sentimento em textos de redes sociais.

## 6.0 Resultados

Os resultados do projeto são os insights gerados e apresentados no dashboard. Através da ferramenta, foi possível observar que:

* (Exemplo de insight) A especulação sobre "Mega Dragonite" e "Mega Hawlucha" foi recebida com um volume muito maior de comentários **positivos** em comparação com "Mega Victreebell".
* (Exemplo de insight) O sentimento geral da comunidade sobre o tópico é **majoritariamente positivo**, indicando um alto nível de hype.

Como resultado, foi construído um pipeline de dados completo, capaz de extrair e analisar opiniões de uma comunidade online em tempo real. A ferramenta desenvolvida permite que analistas de marketing ou gerentes de produto possam, de forma rápida e visual, medir a temperatura de uma comunidade e entender quais ideias geram mais engajamento positivo.
