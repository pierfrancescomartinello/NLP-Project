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
