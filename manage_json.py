import json


def create_json(academic_papers):
    with open('academic_papers.json', 'w', encoding='utf-8') as json_file:
        json.dump(academic_papers, json_file, ensure_ascii=False, indent=4)

def load_json():
    with open('academic_papers.json', 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)
    return data


def create_inverted_json(inverted_index):
    with open('inverted_index.json', 'w', encoding='utf-8') as json_file:
        json.dump(inverted_index, json_file, ensure_ascii=False, indent=4)

def load_inverted_json():
    with open('inverted_index.json', 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)
    return data


def create_ranking_json(ranking_papers):
    with open('ranking_papers.json', 'w', encoding='utf-8') as json_file:
        json.dump(ranking_papers, json_file, ensure_ascii=False, indent=4)

def load_ranking_json():
    with open('ranking_papers.json', 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)
    return data
