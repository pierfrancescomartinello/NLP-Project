from typing import Callable
from bs4 import BeautifulSoup
import requests
import hashlib

from .preprocessor import remove_linebreak


class Crawler:
    max_depth: int
    _cur_depth: int = 1
    root: str
    _links: list[str]
    _visited: list[str] # Contains the URLs already visited, Python already works with hashes when dealing with search in lists
    strategy: Callable

    def fetch_page(self, link: str) -> BeautifulSoup:
        res = requests.get(link)
        return BeautifulSoup(res.content, "lxml")

    def fetch_links(self, soup: BeautifulSoup) -> list[str]:
        return [a['href'] for a in soup.find_all("a", href=True)]

    def fetch_articles(self, soup: BeautifulSoup, link: str) -> list[str]:
        soup = self.fetch_page(link)
        texts = []

        for art in soup.find_all("article"):
            paragraphs = art.find_all("p")
            text = "".join(remove_linebreak(p.get_text()) for p in paragraphs)
            texts.append(text)

        return texts

    def Crawler(max_depth, root, strategy):
        self.max_depth = max_depth;
        self
        pass


if __name__ == "__main__":
    c = Crawler()
    bs = c.fetch_page( "hi")
    c.fetch_articles(bs)
    c.fetch_links(bs)