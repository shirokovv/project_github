import json

import requests
from bs4 import BeautifulSoup
import pymorphy2

from parse.config import WORDS_TO_ACCEPT
from parse.models import Page, Data


def parse_parent(url: str, pages: int = 1):
    Page.objects.all().delete()
    Data.objects.all().delete()

    crawl_url = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    crawl_url.raise_for_status()

    for i in range(pages):
        soup = BeautifulSoup(crawl_url.text, 'lxml')

        button_to_load = soup.find('div', id='_id_showmorebtn')
        for div in soup.find_all("div", {"class": "m_techlisting"}):
            i += 1
            select_a = div.find('a')
            parse_link(select_a['href'])

        next_link_attrs = button_to_load.select_one('a').attrs

        if i == pages - 1:
            break
        crawl_url = requests.get(url + f'index.shtml?p=main&d={next_link_attrs["data-d"]}&not_in={next_link_attrs["data-not_in"]}',
                                 headers={'User-Agent': 'Mozilla/5.0'})
        crawl_url.raise_for_status()

    group_results()


def format_text(text: str):
    symbols = [',', '.', '"', '-', ':', '/', '(', ')', '[', ']', '{', '}', '«', '»', '—', '\xa0', '\n']

    for s in symbols:
        text = text.replace(s, ' ')

    return text


def parse_link(url: str, base_url: str = 'https://www.gazeta.ru'):
    crawl_url = requests.get(base_url + url, headers={'User-Agent': 'Mozilla/5.0'})
    crawl_url.raise_for_status()

    soup = BeautifulSoup(crawl_url.text, 'lxml')

    title = soup.find('h1', {'class': 'headline'}).text
    category = url[1:url[1:].find('/') + 1]

    paragraphs = soup.find('div', {'class': 'b_article-text'})
    text = paragraphs.text
    text_formatted = format_text(text).split(' ')

    morph = pymorphy2.MorphAnalyzer()

    words = {}

    for word in text_formatted:
        if not word:
            continue
        word_parsed = morph.parse(word)[0]

        if word_parsed.tag.POS not in WORDS_TO_ACCEPT:
            continue

        normal_form = word_parsed.normal_form
        if normal_form in words:
            words[normal_form] += 1
        else:
            words[normal_form] = 1

    page = Page(
        link=base_url + url,
        title=title,
        category=category,
        raw_text=text,
        dictionary=json.dumps(words)
    )

    page.save()


def group_results():
    stats = {
        'all': {}
    }

    stats_values = {
        'all': 0
    }

    pages = Page.objects.all()

    for page in pages:
        stats_values['all'] += 1
        if page.category in stats_values:
            stats_values[page.category] += 1
        else:
            stats_values[page.category] = 1

        insert_new = page.category in stats
        if not insert_new:
            stats[page.category] = json.loads(page.dictionary)

        for (key, value) in json.loads(page.dictionary).items():

            if key in stats['all']:
                stats['all'][key] += value
            else:
                stats['all'][key] = value

            if not insert_new:
                continue

            if key in stats[page.category]:
                stats[page.category][key] += value
            else:
                stats[page.category][key] = value

    for (key, value) in stats.items():
        sorted_stat = [{k: v} for k, v in sorted(value.items(), key=lambda item: -item[1])]
        Data(category=key,
             dictionary=sorted_stat,
             quantity=stats_values[key]
             ).save()
