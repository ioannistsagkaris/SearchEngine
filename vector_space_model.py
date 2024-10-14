from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from manage_json import create_ranking_json, load_json


def vectorize_documents(documents):
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(documents)
    return vectorizer, tfidf_matrix


def rank_documents(query, vectorizer, tfidf_matrix, documents):
    query_vector = vectorizer.transform([query])
    cosine_similarities = cosine_similarity(query_vector, tfidf_matrix).flatten()
    document_scores = list(zip(range(len(documents)), cosine_similarities))
    sorted_documents = sorted(document_scores, key=lambda x: x[1], reverse=True)
    return sorted_documents


def list_ranked_documents(sorted_documents, documents):
    list = []
    for index, score in sorted_documents:
        title = documents[index]['Title']
        authors = documents[index]['Authors']
        abstract = documents[index]['Abstract']
        pub_date = documents[index]['Publication date']
        link = documents[index]['Link']
        
        list.append({
            'Title': title,
            'Authors': authors,
            'Abstract': abstract,
            'Publication date': pub_date,
            'Link': link,
            'Score': score
        })

    create_ranking_json(list)


def vsm(query):
    data = load_json()

    titles = [entry['Title'] for entry in data]
    abstracts = [entry['Abstract'] for entry in data]
    documents = [title + ' ' + abstract for title, abstract in zip(titles, abstracts)]

    vectorizer, tfidf_matrix = vectorize_documents(documents)

    ranked_documents = rank_documents(query, vectorizer, tfidf_matrix, documents)
    list_ranked_documents(ranked_documents, data)
