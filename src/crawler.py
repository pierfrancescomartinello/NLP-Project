from typing import Callable
from bs4 import BeautifulSoup
import requests

from .preprocessor import remove_linebreak


class Crawler:
    max_depth: int
    _cur_depth: int = 0
    root: str
    _links: set[str] = set()
    _visited: set[str] = set() # Contains the URLs already visited, Python already works with hashes when dealing with search in sets
    strategy: Callable

    def _bfs(self):
        pass

    def _dfs(self):
        pass

    _funcs = {
        "dfs": _dfs(),
        "bfs": _bfs(),
    }

    def __init__(self, max_depth, root, strategy):
        self.max_depth = max_depth
        self.root = root
        self.strategy = strategy
        self._links = set(root)


    def _fetch_page(self, link: str) -> BeautifulSoup:
        res = requests.get(link)
        return BeautifulSoup(res.content, "lxml")

    def _fetch_links(self, soup: BeautifulSoup) -> list[str]:
        return set(a['href'] for a in soup.find_all("a", href=True))

    def _fetch_articles(self, soup: BeautifulSoup, link: str) -> list[str]:
        soup = self.fetch_page(link)
        texts = []

        for art in soup.find_all("article"):
            paragraphs = art.find_all("p")
            text = "".join(remove_linebreak(p.get_text()) for p in paragraphs)
            texts.append(text)

        return texts

    def _URL_list_merging(_visited:set[str], fetched_links:set[str]):
        return list(set(fetched_links) - _visited)

    def URL_cleaning():
        pass
if __name__ == "__main__":
    c = Crawler()
    bs = c.fetch_page("hi")
    c.fetch_articles(bs)
    c.fetch_links(bs)