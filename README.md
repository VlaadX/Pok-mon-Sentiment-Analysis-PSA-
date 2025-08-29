## **Análise de Sentimento da Comunidade "To Be Hero X"**

![Capa do Projeto](https://github.com/VlaadX/Pok-mon-Sentiment-Analysis-PSA-/blob/main/imgs/cover_img.jpg)

A **análise de sentimento**, também conhecida como mineração de opinião, é uma técnica de Processamento de Linguagem Natural (PLN) usada para determinar o tom emocional expresso em um texto. O objetivo é entender se o texto transmite um sentimento **positivo**, **negativo** ou **neutro**.

No contexto de séries de anime e produções audiovisuais, a análise de sentimento é crucial para:

* **Análise de Feedback da Comunidade:** Entender a recepção de novos episódios, arcos de história e desenvolvimento de personagens.
* **Monitoramento de Engajamento:** Acompanhar a percepção pública da série e de seus personagens principais.
* **Pesquisa de Roteiro:** Identificar quais arcos ou personagens geram mais discussões e como os fãs estão reagindo a eles em tempo real.
* **Gerenciamento de Comunidade:** Detectar rapidamente focos de insatisfação ou hype na fanbase.

Neste projeto, analisamos o sentimento da comunidade de fãs do anime **To Be Hero X**. Os dados para análise foram coletados em tempo real de discussões na plataforma Reddit para mapear a opinião pública sobre os personagens e a evolução da série ao longo dos episódios.

---
## **1.0 Problema de Negócio**

Uma produtora de anime, um serviço de streaming ou mesmo um fã-clube engajado precisa entender o impacto de sua obra na audiência. Com uma série em andamento como "To Be Hero X", surgem questões de negócio fundamentais: **Qual a recepção dos personagens principais pela comunidade?** e **Como o sentimento dos fãs evoluiu ao longo da temporada?**

Uma resposta baseada em dados a essas perguntas pode influenciar campanhas de marketing, estratégias de conteúdo para redes sociais e até mesmo fornecer insights para futuras temporadas. Utilizando métodos de PLN e web scraping, foi construído um pipeline de dados capaz de coletar, processar e analisar milhares de comentários de fãs. A solução final é um **dashboard interativo de múltiplas páginas** construído com Streamlit, permitindo uma consulta rápida e visual dos resultados.

---
## **2.0 Fonte dos Dados**

Os dados não vieram de um dataset estático, mas foram coletados diretamente da API do Reddit usando a biblioteca `PRAW` em Python.

* **Fonte:** Comentários em posts do subreddit oficial da série.
* **Subreddit Alvo:** `r/ToBeHero_X`.
* **Dados Coletados:** Corpo do comentário, título do post, subreddit de origem, pontuação do comentário, e o episódio de discussão (quando aplicável).

---
## **3.0 Estratégia da Solução**

O projeto foi estruturado em um pipeline claro, desde a coleta de dados brutos até a apresentação de insights em um dashboard interativo.

1.  **Coleta de Dados:** Foram desenvolvidos dois scripts Python especializados:
    * `coletor_herois.py`: Busca comentários que mencionam especificamente os nomes dos personagens principais.
    * `coletor_episodios.py`: Busca todos os comentários dentro dos posts de discussão de cada episódio da série.
2.  **Pré-processamento e Análise de Sentimento:** Um terceiro script (`analisador_sentimento.py`) processa os dados brutos coletados.
    * **Limpeza:** Os textos dos comentários foram limpos para remover ruídos como links e caracteres especiais.
    * **Análise:** Foi utilizado o modelo de linguagem pré-treinado **`cardiffnlp/twitter-roberta-base-sentiment-latest`** da plataforma Hugging Face. Este modelo, baseado na arquitetura RoBERTa, é especializado em classificar sentimentos em textos de redes sociais.
3.  **Extração de Insights:** Um script final de análise (`analise_herois_por_episodio.py`) cruza os dados dos dois CSVs para determinar qual personagem foi o mais comentado em cada episódio.
4.  **Dashboard Interativo:** Todos os componentes foram integrados em uma aplicação web (`dashboard.py` e a pasta `pages/`) com Streamlit. O dashboard possui duas seções principais para permitir que um usuário final filtre e explore os dados de forma intuitiva.

---
## **4.0 Tecnologias Utilizadas**

* **Linguagem:** Python 3.10
* **Coleta de Dados:** PRAW (Python Reddit API Wrapper)
* **Análise de Dados:** Pandas
* **NLP / Análise de Sentimento:** Hugging Face Transformers (RoBERTa)
* **Visualização de Dados:** Plotly
* **Dashboard:** Streamlit
* **Gerenciamento de Credenciais:** python-dotenv

---
## **5.0 Visão Geral da Aplicação**

O resultado final é um dashboard interativo de múltiplas páginas que consolida todos os insights.

#### **Página Principal**
A página inicial oferece uma visão geral do projeto e métricas agregadas de todos os dados coletados.
![Página Principal do Dashboard](https://github.com/VlaadX/Pok-mon-Sentiment-Analysis-PSA-/blob/main/imgs/screenshot_main_page.PNG)


#### **Análise por Herói**
Esta página permite uma análise detalhada da recepção de cada personagem, com um gráfico comparativo do sentimento associado a cada um.
![Página de Análise por Herói](https://github.com/VlaadX/Pok-mon-Sentiment-Analysis-PSA-/blob/main/imgs/screenshot_hero_analysis.PNG)


#### **Análise por Episódio**
Aqui, é possível acompanhar a evolução do sentimento da comunidade ao longo do tempo. Um gráfico de linhas mostra as flutuações de comentários positivos, neutros e negativos a cada novo episódio.
![Gráfico de Linhas - Sentimento por Episódio](https://github.com/VlaadX/Pok-mon-Sentiment-Analysis-PSA-/blob/main/imgs/screenshot_episode_line_chart.PNG)



---
## **6.0 Resultados e Insights**

Através da ferramenta, foi possível extrair insights valiosos sobre a comunidade:

* **Personagens Dominantes e Polêmicos:** Personagens como **Queen** e **Ghostblade** dominam o volume de discussões, mas também são os mais polarizantes, atraindo uma quantidade significativa de comentários negativos junto com o engajamento.
* **Evolução da Recepção:** A análise temporal revelou picos de sentimento negativo em episódios específicos, que podem ser correlacionados com eventos controversos na trama, como a morte de um personagem ou um *plot twist* mal recebido.
* **Natureza da Discussão:** O sentimento geral da comunidade é majoritariamente **Neutro**, indicando que grande parte da discussão é focada em análise da história, teorias e descrições de eventos, caracterizando uma fanbase analítica e engajada.

Como resultado, foi construído um pipeline de dados completo, capaz de extrair e analisar opiniões de uma comunidade online em tempo real. A ferramenta desenvolvida permite que analistas, criadores de conteúdo ou gerentes de produto possam, de forma rápida e visual, **"medir a temperatura"** da comunidade e tomar decisões mais informadas.

---
## **7.0 Como Executar o Projeto**

1.  **Clone o repositório:**
    ```bash
    git clone https://github.com/VlaadX/ToBeHeroX-Sentiment-Analysis.git
    cd seu-repositorio
    ```
2.  **Crie e ative um ambiente virtual:**
    ```bash
    python -m venv venv
    # Windows
    .\venv\Scripts\activate
    # macOS/Linux
    source venv/bin/activate
    ```
3.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Configure as credenciais:**
    * Renomeie o arquivo `.env.example` para `.env`.
    * Preencha o arquivo `.env` com suas credenciais da API do Reddit.
5.  **Execute os scripts de coleta e análise (na ordem):**
    ```bash
    python coletor_herois.py
    python coletor_episodios.py
    python analisador_sentimento.py # Execute-o para os dois CSVs
    python analise_herois_por_episodio.py
    ```
6.  **Inicie o Dashboard:**
    ```bash
    streamlit run dashboard.py
    ```
