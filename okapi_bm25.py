from rank_bm25 import BM25Okapi
from manage_json import create_ranking_json, load_json


def rank_articles(query, corpus):
    tokenized_corpus = [article['Title'].lower().split() for article in corpus]
    bm25 = BM25Okapi(tokenized_corpus)
    scores = bm25.get_scores(query.lower().split())
    ranked_articles = sorted(zip(scores, range(len(scores))), reverse=True)
    return ranked_articles


def list_ranked_articles(ranked_articles, corpus):
    list = []
    for score, index in ranked_articles:
        title = corpus[index]['Title']
        authors = corpus[index]['Authors']
        abstract = corpus[index]['Abstract']
        pub_date = corpus[index]['Publication date']
        link = corpus[index]['Link']

        list.append({
            'Title': title,
            'Authors': authors,
            'Abstract': abstract,
            'Publication date': pub_date,
            'Link': link,
            'Score': score
        })
    
    create_ranking_json(list)


def okapi(query):
    corpus = load_json()

    ranked_articles = rank_articles(query, corpus)
    list_ranked_articles(ranked_articles, corpus)
