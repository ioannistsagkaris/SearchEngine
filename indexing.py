from text_processing import process_text


class Indexer:
    def __init__(self):
        self.inverted_index = {}


    def index_document(self, title, abstract, id_count):
        tokens = process_text(title, abstract)

        for term in tokens:
            if term in self.inverted_index:
                if 'articles' in self.inverted_index[term]:
                    entry_exists = any(article['ID'] == id_count for article in self.inverted_index[term]['articles'])
                    if entry_exists:
                        for article in self.inverted_index[term]['articles']:
                            if article['ID'] == id_count:
                                article['appearances'] += 1
                    else:
                        self.inverted_index[term]['articles'].append({'ID': id_count, 'appearances': 1})
                else:
                    self.inverted_index[term]['articles'] = [{'ID': id_count, 'appearances': 1}]
            else:
                self.inverted_index[term] = {'articles': [{'ID': id_count, 'appearances': 1}]}


    def get_inverted_index(self):
        return self.inverted_index
