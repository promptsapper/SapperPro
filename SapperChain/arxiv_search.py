#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# import arxiv
#
# search = arxiv.Search(
#     query="generative AI for code generation",
#     max_results=10,
#     sort_by=arxiv.SortCriterion.SubmittedDate
# )
#
# for result in search.results():
#     print(result.entry_id, '->', result.title)

import requests
from bs4 import BeautifulSoup


def get_papers(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    papers = []
    for paper in soup.find_all('div', class_='paper'):
        title = paper.find('h2').text
        authors = paper.find('p', class_='authors').text
        abstract = paper.find('p', class_='abstract').text
        papers.append({'title': title, 'authors': authors, 'abstract': abstract})

    return papers


base_url = 'https://www.icse2023.org'
icse_url = base_url + '/program/main-conference'
ase_url = base_url + '/program/ase'
fse_url = base_url + '/program/fse'

icse_papers = get_papers(icse_url)
ase_papers = get_papers(ase_url)
fse_papers = get_papers(fse_url)

all_papers = icse_papers + ase_papers + fse_papers

# Filter papers with 'generative AI for code' in their titles or abstracts
generative_ai_papers = [paper for paper in all_papers if
                        'generative AI for code' in paper['title'].lower() or 'generative AI for code' in paper[
                            'abstract'].lower()]

for paper in generative_ai_papers:
    print('Title:', paper['title'])
    print('Authors:', paper['authors'])
    print('Abstract:', paper['abstract'])
    print('-' * 50)

