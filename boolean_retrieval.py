import re
from nltk.stem import PorterStemmer
from manage_json import *


def apply_boolean_operator(operator, result1, result2):
    ids1 = set(article['ID'] for article in result1)
    ids2 = set(article['ID'] for article in result2)

    if operator == 'AND':
        common_ids = ids1 & ids2
        return [article for article in result1 + result2 if article['ID'] in common_ids]
    elif operator == 'OR':
        return [article for article in result1 + result2]
    elif operator == 'NOT':
        ids_diff = ids1 - ids2
        return [article for article in result1 if article['ID'] in ids_diff]
    else:
        raise ValueError(f'Unsupported boolean operator: {operator}')


def parse_query(query):
    terms_and_operators = re.findall(r'\b(?:AND|OR|NOT|\w+)\b', query.upper())
    terms = [term.lower() for term in terms_and_operators if term not in ('AND', 'OR', 'NOT')]
    operators = [op for op in terms_and_operators if op in ('AND', 'OR', 'NOT')]
    return terms, operators


def stem_query_terms(terms):
    stemmer = PorterStemmer()
    return [stemmer.stem(term) for term in terms]


def search(json_data, query):
    terms, operators = parse_query(query)
    stemmed_terms = stem_query_terms(terms)
    result = json_data.get(stemmed_terms[0], {'articles': []})['articles']
    term_appearances = {term: set(article['ID'] for article in result) for term in stemmed_terms}

    for i in range(1, len(stemmed_terms)):
        next_term = json_data.get(stemmed_terms[i], {'articles': []})['articles']
        term_appearances[stemmed_terms[i]] = set(article['ID'] for article in next_term)
        result = apply_boolean_operator(operators[i - 1], result, next_term)

    unique_results = list(set(article['ID'] for article in result))
    list_ranked_documents(unique_results)


def list_ranked_documents(unique_results):
    list = []
    academic_data = load_json()
    for unique_id in unique_results:
        matching_entry = next((entry for entry in academic_data if entry['ID'] == unique_id), None)
    
        if matching_entry:
            title = matching_entry['Title']
            authors = matching_entry['Authors']
            abstract = matching_entry['Abstract']
            pub_date = matching_entry['Publication date']
            link = matching_entry['Link']
            
            list.append({
                'ID': unique_id,
                'Title': title,
                'Authors': authors,
                'Abstract': abstract,
                'Publication date': pub_date,
                'Link': link,
            })
    create_ranking_json(list)


def bln_rtrvl(query):
    json_data = load_inverted_json()
    search(json_data, query)
