import string
import bs4
import os
import re
import json
from html.parser import HTMLParser

'''
now only try to modify a single html file.
without css modifying & zipfile
'''

def modify_html_file(file_name) -> None:
    html_file = open(file_name, 'r', encoding='utf-8')
    bs = bs4.BeautifulSoup(html_file.read(), 'html5lib')

    # remove tables
    tables = bs.find_all('table')
    for table in tables:
        table.decompose()

    # remove class for all imgs
    imgs = bs.find_all('img')
    for img in imgs:
        del img['class']

    # modify all comments for imgs
    first_comment = bs.find_all('img')[0].parent.next_sibling.next_sibling
    spans = first_comment.find_all('span')
    class1 = spans[0]['class'][0]
    class2 = spans[1]['class'][0]
    count = False
    for im in bs.find_all('img'):
        if count == False:
            count = True
            continue
        comment = im.parent.next_sibling.next_sibling
        text = comment.get_text()
        comment.clear()
        span1 = bs.new_tag('span', attrs={'class': class1})
        span2 = bs.new_tag('span', attrs={'class': class2})
        span2.string = text
        comment.insert(0, span1)
        span1.insert(0, span2)

    new_html_file = open('./before/new_002.html', 'w', encoding='utf-8')
    new_html_file.write(bs.prettify())

    html_file.close()
    new_html_file.close()


def get_sections() -> dict:
    # get all sections
    sections = {}
    section_page_file = open(
        './before/index_split_000.html', 'r', encoding='utf-8')
    s_bs = bs4.BeautifulSoup(section_page_file.read(), 'html5lib')
    for section in s_bs.find_all('li'):
        sections[section.get_text()] = []
    all_file = os.listdir('./before/')
    for f in all_file:
        if re.match('index_split_(.)+.html', f) and f != 'index_split_000.html':
            bbbs = bs4.BeautifulSoup(open('./before/'+f, encoding='utf-8').read(),
                                     'html5lib')
            sctn = bbbs.find('h2')
            if sctn == None or sctn.get_text() not in sections:
                continue
            posts = bbbs.find_all('li')
            for post in posts:
                sections[sctn.get_text()].append(post.get_text())
    return sections


def modify_css_file(file_name) -> None:
    # import files
    css_file = open('./before/stylesheet.css', 'r+', encoding='utf-8')
    add_css_file = open('./add_css.css', 'r', encoding='utf-8')
    old = css_file.read()
    if old[:3] != 'img':  # for test
        add_css = add_css_file.read()
        css_file.seek(0)
        css_file.write(add_css)
        css_file.write(old)
    css_file.close()
    add_css_file.close()

if __name__ == '__main__':
    123