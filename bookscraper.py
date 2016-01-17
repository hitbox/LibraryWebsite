import argparse
import operator
import requests
import urlparse

from bs4 import BeautifulSoup as BS
from pprint import pprint as pp

__all__ = ['scrapebook']

KENTON_URL = 'http://catalog.kentonlibrary.org/eg/opac/results'

def _add_book_data(book, soup, url):
    """
    Modify book in-place with details from soup
    """
    # title
    title = book['title'] = soup.find(id='rdetail_title')
    if title:
        book['title'] = title.string

    # authors
    authors = book['authors'] = []
    for tag in soup.select('.rdetail-author-div'):
        authors.append(''.join(tag.stripped_strings))

    def detailgetter(tag):
        key = tag.select_one('.rdetail_label')
        if key:
            key = key.string.rstrip(':')

        value = tag.select_one('.rdetail_value')
        if value:
            value = value.string

        return (key, value)

    # book details
    details = book['details'] = {}
    for tag in soup.find(id='rdetail_record_details').find('ul').find_all('li'):
        key, val = detailgetter(tag)
        if not (key or val):
            continue

        if key in details:
            try:
                details.append(val)
            except AttributeError:
                details[key] = [ details[key], val ]
        else:
            details[key] = val

    # images
    imagetag = soup.find(id='rdetail_image')
    if imagetag:
        book['image_medium'] = urlparse.urljoin(url, imagetag['src'])
        book['image_large'] = urlparse.urljoin(url, imagetag.parent['href'])

def scrapebook(isbn, url=None):
    """
    Scrape book information from the Kenton County Library Catalog website.

    Returns a dictionary of data scraped. An empty dictionary if not found.
    """
    if url is None:
        url = KENTON_URL

    book = {}

    result = requests.get(url, params=dict(query=isbn, qtype='keyword'))
    if result:
        soup = BS(result.text, 'lxml')
        _add_book_data(book, soup, url)

        if 'details' in book and 'ISBN' in book['details']:
            # check that one of the ISBNs equal the ISBN we searched for
            isbns = book['details']['ISBN']

            # wrap in a list if string
            if isinstance(isbns, basestring):
                isbns = [isbns]

            for value in isbns:
                if isbn in value.split():
                    break
            else:
                book = {}

    return book


def ArgParser():
    p = argparse.ArgumentParser(description='Scrape book information')
    _a = p.add_argument
    _a('isbn', help='ISBN number to search for')
    return p

def main():
    parser = ArgParser()
    args = parser.parse_args()
    book = scrapebook(args.isbn)
    if book:
        pp(book)


if __name__ == '__main__':
    main()
