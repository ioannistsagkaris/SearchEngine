from tkinter import ttk
from boolean_retrieval import bln_rtrvl
from okapi_bm25 import okapi
from vector_space_model import vsm
from web_crawler import *
import tkinter as tk
from manage_json import load_ranking_json


def search(option):
    url = 'https://arxiv.org/search/'
    query = entry.get()
    author_combobox.set('Select Author')
    year_combobox.set('Select Year')
    
    list = fetch_page(url, query)
    if list == None:
        print('There was an error while fetching the articles from the page!')
        return None
    
    if option == 'boolean':
       bln_rtrvl(query)
    elif option == 'vsm':
        vsm(query)
    elif option == 'okapi':
        okapi(query)

    load()


def update():
    global default_option
    option = default_option.get()
    return option


def load():
    try:
        data = load_ranking_json()
        formatted_data = []

        years = set()
        authors_set = set()

        for item in data:
            title = item.get('Title')
            authors = ', '.join(item.get('Authors'))
            abstract = item.get('Abstract')
            pub_date = item.get('Publication date')
            link = item.get('Link')
            score = item.get('Score')

            for author in item.get('Authors'):
                authors_set.add(author)

            year = pub_date.split()[-1]
            years.add(year)

            formatted_data.append(
                f'Title: {title}\n'
                f'Authors: {authors}\n'
                f'Abstract: {abstract}\n'
                f'Publication date: {pub_date}\n'
                f'Link: {link}\n'
                f'Score: {score}\n\n'
            )

        year_combobox['values'] = sorted(list(years))
        author_combobox['values'] = sorted(list(authors_set))

        text_widget.config(state=tk.NORMAL)
        text_widget.delete(1.0, tk.END)
        text_widget.insert(tk.END, '\n'.join(formatted_data))
        text_widget.config(state=tk.DISABLED)

    except FileNotFoundError:
        text_widget.config(state=tk.NORMAL)
        text_widget.delete(1.0, tk.END)
        text_widget.insert(tk.END, 'File not found.')
        text_widget.config(state=tk.DISABLED)


def filter_by_year(selected_year):
    author_combobox.set('Select Author')
    try:
        data = load_ranking_json()
        formatted_data = []

        for item in data:
            title = item.get('Title')
            authors = ', '.join(item.get('Authors'))
            abstract = item.get('Abstract')
            pub_date = item.get('Publication date')
            link = item.get('Link')
            score = item.get('Score')

            year = pub_date.split()[-1]

            if year == selected_year:
                formatted_data.append(
                    f'Title: {title}\n'
                    f'Authors: {authors}\n'
                    f'Abstract: {abstract}\n'
                    f'Publication date: {pub_date}\n'
                    f'Link: {link}\n'
                    f'Score: {score}\n\n'
                )

        text_widget.config(state=tk.NORMAL)
        text_widget.delete(1.0, tk.END)

        if formatted_data:
            text_widget.insert(tk.END, '\n'.join(formatted_data))
        else:
            text_widget.insert(tk.END, f'No articles found for the year {selected_year}')

        text_widget.config(state=tk.DISABLED)

    except FileNotFoundError:
        text_widget.config(state=tk.NORMAL)
        text_widget.delete(1.0, tk.END)
        text_widget.insert(tk.END, 'File not found.')
        text_widget.config(state=tk.DISABLED)


def filter_by_author(selected_author):
    year_combobox.set('Select Year')

    try:
        data = load_ranking_json()
        formatted_data = []

        for item in data:
            title = item.get('Title')
            authors = ', '.join(item.get('Authors'))
            abstract = item.get('Abstract')
            pub_date = item.get('Publication date')
            link = item.get('Link')
            score = item.get('Score')

            if selected_author.lower() in authors.lower():
                formatted_data.append(
                    f'Title: {title}\n'
                    f'Authors: {authors}\n'
                    f'Abstract: {abstract}\n'
                    f'Publication date: {pub_date}\n'
                    f'Link: {link}\n'
                    f'Score: {score}\n\n'
                )

        text_widget.config(state=tk.NORMAL)
        text_widget.delete(1.0, tk.END)

        if formatted_data:
            text_widget.insert(tk.END, '\n'.join(formatted_data))
        else:
            text_widget.insert(tk.END, f'No articles found for the author {selected_author}')

        text_widget.config(state=tk.DISABLED)

    except FileNotFoundError:
        text_widget.config(state=tk.NORMAL)
        text_widget.delete(1.0, tk.END)
        text_widget.insert(tk.END, 'File not found.')
        text_widget.config(state=tk.DISABLED)


app = tk.Tk()
app.title('Search Engine')

window_width = 1500
window_height = 1000
screen_width = app.winfo_screenwidth()
screen_height = app.winfo_screenheight()
x_position = (screen_width - window_width) // 2
y_position = (screen_height - window_height) // 2
app.geometry(f'{window_width}x{window_height}+{x_position}+{y_position}')
#app.resizable(False, False)

title_label = tk.Label(app, text='Search Engine', font=('Arial', 20))
title_label.place(relx=0.1, rely=0.02, anchor=tk.CENTER)

entry = tk.Entry(app, width=80, font=('Arial', 14))
entry.place(relx=0.5, rely=0.02, anchor=tk.CENTER)

default_option = tk.StringVar(value='vsm')
option1 = tk.Radiobutton(app, text='Boolean Retrieval', variable=default_option, value='boolean', font=('Arial', 12), command=update)
option2 = tk.Radiobutton(app, text='Vector Space Model', variable=default_option, value='vsm', font=('Arial', 12), command=update)
option3 = tk.Radiobutton(app, text='Okapi BM25', variable=default_option, value='okapi', font=('Arial', 12), command=update)
option1.place(relx=0.325, rely=0.06, anchor=tk.CENTER)
option2.place(relx=0.5, rely=0.06, anchor=tk.CENTER)
option3.place(relx=0.68, rely=0.06, anchor=tk.CENTER)

year_combobox = ttk.Combobox(app, state='readonly')
year_combobox.place(relx=0.9, rely=0.06, anchor=tk.CENTER)
year_combobox.set('Select Year')
year_combobox.bind('<<ComboboxSelected>>', lambda event: filter_by_year(year_combobox.get()))

author_combobox = ttk.Combobox(app, state='readonly')
author_combobox.place(relx=0.9, rely=0.095, anchor=tk.CENTER)
author_combobox.set('Select Author')
author_combobox.bind('<<ComboboxSelected>>', lambda event: filter_by_author(author_combobox.get()))

search_button = tk.Button(app, text='Search', command=lambda: search(update()), font=('Arial', 14))
search_button.place(relx=0.9, rely=0.02, anchor=tk.CENTER)

result_label = tk.Label(app, text='', font=('Arial', 14))
result_label.place(relx=0.5, rely=0.8, anchor=tk.CENTER)

text_widget = tk.Text(app, wrap=tk.WORD, width=210, height=67, state=tk.DISABLED)
text_widget.place(relx=0.5, rely= 0.555, anchor=tk.CENTER)

app.mainloop()
