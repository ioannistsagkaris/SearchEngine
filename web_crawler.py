import requests
from bs4 import BeautifulSoup
from indexing import Indexer
from manage_json import *
from text_processing import process_text


def fetch_page(url, query):

    id_count = 1
    num_pages = 5
    academic_papers = []
    index = Indexer()

    for page in range(num_pages):
        target_url = f'{url}?query={query}&searchtype=all&order=-announced_date_first&size=100&start={page * 100}'

        response = requests.get(target_url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            articles = soup.find_all('li', class_='arxiv-result')

            for article in articles:
                title = article.find('p', class_='title is-5 mathjax').text.strip()
                authors_container = article.find('p', class_='authors')
                if authors_container:
                    authors = [author.text.strip() for author in authors_container.find_all('a')]
                abstract_tag = article.find('span', class_='abstract-full has-text-grey-dark mathjax')
                abstract = ''.join([text for text in abstract_tag.find_all(text=True, recursive=True) if text.parent.name != 'a']).strip()
                date = article.find('p', class_='is-size-7').find('span', class_='has-text-black-bis has-text-weight-semibold').next_sibling.split(';')[0].strip()
                link = article.find('a', href=lambda x: x and 'pdf' in x)['href'] if article.find('a', href=lambda x: x and 'pdf' in x) else None

                academic_papers.append({
                    'ID' : id_count,
                    'Title': title,
                    'Authors': authors,
                    'Abstract': abstract,
                    'Publication date': date,
                    'Link': link
                })

                index.index_document(title, abstract, id_count)
            
                id_count += 1
        else:
            return None
    
    create_json(academic_papers)
    inverted_index = index.get_inverted_index()
    create_inverted_json(inverted_index)
    return academic_papers
