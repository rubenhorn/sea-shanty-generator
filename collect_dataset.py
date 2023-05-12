#! /usr/bin/env python3

from bs4 import BeautifulSoup
from bs4.element import Tag
import json, re, requests, sys

SHANTY_LIST_URL = 'https://shanty.rendance.org/lyrics/shanties.php'


def http_get(url):
    """Get the contents of a url pretending to be cURL."""
    r = requests.get(url, headers={'User-Agent': 'curl/7.64.1'})
    return BeautifulSoup(r.text, features='html.parser')


def get_shanty_links():
    """Get a list of shanties and their urls."""
    soup = http_get(SHANTY_LIST_URL)
    # div (id=...) > ul > li > a
    tags = ['contentleft', 'contentright']
    def get_shanty_links(s, id): return [c.contents[0] for c in s.find(
        id=id).contents[1].contents if isinstance(c, Tag)]
    shanty_links = [s for t in tags for s in get_shanty_links(soup, t)]
    base_url = SHANTY_LIST_URL[:SHANTY_LIST_URL.rfind('/') + 1]
    shanty_urls = {s.contents[0]
        : f'{base_url}{s["href"]}' for s in shanty_links}
    return shanty_urls


def get_shanty(shanty_url):
    """Get the lyrics of a shanty."""
    soup = http_get(shanty_url)
    shanty = soup.find('div', {'class': 'lyrics'})
    text = '\n'.join([l.strip() for l in shanty.text.strip().split('\n')])
    # Indicate new verse with indentation
    return re.sub(r'\n{2,}', '\n\t', text)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(
            f'Usage: python3 {sys.argv[0]} <generated json file>', file=sys.stderr)
        sys.exit(1)

    def download_shanties(shanty_urls):
        for shanty, url in shanty_urls.items():
            print(f' - {shanty}...', file=sys.stderr, end='', flush=True)
            yield get_shanty(url)
            print('done', file=sys.stderr)
    print('Downloading shanties', file=sys.stderr)
    shanties = download_shanties(get_shanty_links())
    shanties_json = json.dumps([{'text': s} for s in shanties], indent=4)
    print(f'\nWriting to {sys.argv[1]}...',
          file=sys.stderr, end='', flush=True)
    with open(sys.argv[1], 'w') as f:
        f.write(shanties_json)
    print('done', file=sys.stderr)
