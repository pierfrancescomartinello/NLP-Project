from typing import Callable
from bs4 import BeautifulSoup
import requests

from .preprocessor import remove_linebreak


class Crawler:
    root: str
    links: list[str]
    strategy: str
    max_depth: int
    cur_depth: int

    def _bfs(self):
        pass

    def _dfs(self):
        pass

    _funcs = {
        "dfs": _dfs(),
        "bfs": _bfs(),
    }

    def fetch_page(self, link: str) -> BeautifulSoup:
        res = requests.get(link)
        return BeautifulSoup(res.content, "lxml")

    def crawl(self):
        crawling_func = self._funcs[self.strategy]


if __name__ == "__main__":
    link = "https://www.unipa.it/ateneo/Storia-dellAteneo/index.html"
    link = "https://www.unipa.it/dipartimenti/matematicaeinformatica/cds/dataalgorithmsandmachineintelligence2270/"

    soup = fetch_page(link)
    articles = soup.find_all("article")
    texts = []

    for art in articles:
        paragraphs = art.find_all("p")

        p_text = [remove_linebreak(p.get_text()) for p in paragraphs]
        text = "".join(p_text)
        texts.append(text)

    print(texts)
