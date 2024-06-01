from typing import Callable
from bs4 import BeautifulSoup
import requests
from collections import namedtuple

from preprocessor import remove_linebreak

Link = namedtuple("Link", ["addr", "depth"])


class Crawler:

    max_depth: int
    root: str
    strategy: str
    _do_strategy: Callable
    _links: list[Link] = []
    _visited: set[str] = set()

    def __init__(self, root, max_depth, strategy="bfs"):
        self.max_depth = max_depth
        self.root = root
        self.strategy = strategy
        self._links = [Link(root, 0)]
        self._visited = set()

        _funcs = {
            "dfs": self._dfs_step,
            "bfs": self._bfs_step,
        }

        self._do_strategy = lambda x, y, z: _funcs[self.strategy](x, y, z)

    def _bfs_step(self, x: list, y: list, depth: int):
        y = [Link(el, depth + 1) for el in y]
        return x + y

    def _dfs_step(self, x: list, y: list, depth: int):
        y = [Link(el, depth + 1) for el in y]
        return y + x

    def _fetch_page(self, link: Link) -> BeautifulSoup:
        res = requests.get(link.addr)
        return BeautifulSoup(res.content, "lxml")

    def _fetch_links(self, soup: BeautifulSoup) -> set[str]:
        return set(a["href"] for a in soup.find_all("a", href=True))

    def _fetch_articles(self, soup: BeautifulSoup) -> list[str]:
        texts = []

        for art in soup.find_all("article"):
            paragraphs = art.find_all("p")
            text = "".join(remove_linebreak(p.get_text()) for p in paragraphs)
            texts.append(text)

        return texts

    def crawl(self):
        print(self.strategy)

        articles = []
        while self._links:
            node = self._links.pop()
            if node.addr not in self._visited:
                print(f"\033[32m Depth= {node.depth}, Links: {len(self._links)}, Visited: {len(self._visited)} \033[0m")
                self._visited.add(node.addr)

                soup = self._fetch_page(node)
                articles += self._fetch_articles(soup)

                if node.depth < self.max_depth:
                    neigh_links = self._fetch_links(soup)

                    neigh_links = clean_links(neigh_links)
                    neigh_links = _url_list_merging(self._visited, neigh_links)

                    self._links = self._do_strategy(self._links, neigh_links, node.depth)
            else:
                print("\033[31m Page already visited! \033[0m")
        return articles


def clean_links(links: set):
    return set(
        [
            i
            for i in list(links)
            if "://www.unipa.it" in i and "://www.unipa.it/." not in i
        ]
    )


def _url_list_merging(_visited: set[Link], fetched_links: set[str]):
    return list(fetched_links - _visited)


if __name__ == "__main__":
    c = Crawler(
        root="https://www.unipa.it",
        strategy="bfs",
        max_depth=3,
    )

    articles = c.crawl()
    print(articles)
