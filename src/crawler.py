from typing import Callable
from bs4 import BeautifulSoup
import requests

from .preprocessor import remove_linebreak


class Crawler:
    """
    _visited contains the urls as raw strings, as Python compares hashes when doing string comparison.
    """

    max_depth: int
    root: str
    strategy: Callable
    _cur_depth: int = 0
    _links: list[str] = []
    _visited: set[str] = {}

    def __init__(self, root, max_depth, strategy="bfs"):
        self.max_depth = max_depth
        self.root = root
        self.strategy = strategy
        self._links = [root]

        _funcs = {
            "dfs": self._dfs_step(),
            "bfs": self._bfs_step(),
        }

    def _bfs_step(self):
        pass

    def _dfs_step(self):
        pass

    def _fetch_page(self, link: str) -> BeautifulSoup:
        res = requests.get(link)
        return BeautifulSoup(res.content, "lxml")

    def __fetch_links(self, soup: BeautifulSoup) -> set[str]:
        return set(a["href"] for a in soup.find_all("a", href=True))

    def _fetch_articles(self, soup: BeautifulSoup, link: str) -> list[str]:
        soup = self.fetch_page(link)
        texts = []

        for art in soup.find_all("article"):
            paragraphs = art.find_all("p")
            text = "".join(remove_linebreak(p.get_text()) for p in paragraphs)
            texts.append(text)

        return texts

    def crawl():
        pass

    def _URL_list_merging(_visited:set[str], fetched_links:set[str]):
        return list(set(fetched_links) - _visited)




if __name__ == "__main__":
    c = Crawler(
        root="https://www.unipa.it",
        strategy="bfs",
        max_depth=3,
    )

    bs = c.fetch_page("hi")
    c.fetch_articles(bs)
    c.fetch_links(bs)
    c.fetch_links(bs)
