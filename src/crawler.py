from typing import Callable
from bs4 import BeautifulSoup
import requests

from .preprocessor import remove_linebreak


class Crawler:
    max_depth: int
    cur_depth: int
    root: str
    links: list[str]
    strategy: Callable

    def fetch_page(self, link: str) -> BeautifulSoup:
        res = requests.get(link)
        return BeautifulSoup(res.content, "lxml")

def fetch_links(soup: BeautifulSoup) -> list[str]:
    return [a['href'] for a in soup.find_all("a", href=True)]

def fetch_articles(soup: BeautifulSoup, link: str) -> list[str]:
    soup = fetch_page(link)
    texts = []

    for art in soup.find_all("article"):
        paragraphs = art.find_all("p")
        text = "".join(remove_linebreak(p.get_text()) for p in paragraphs)
        texts.append(text)

    return texts



if __name__ == "__main__":
    bs = fetch_page("hi")
    fetch_articles(bs)
    fetch_links(bs)