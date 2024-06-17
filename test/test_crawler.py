from bs4 import BeautifulSoup
from src.crawler import Crawler, Link
import os
import glob

def test_set_strategy():
    strategy = "bfs"

    c = Crawler(
        "https://ismyinternetworking.com/",
        1,
        strategy=strategy,
    )

    assert c.strategy == strategy


def test_crawl():
    c = Crawler(
        root="https://www.unipa.it",
        strategy="bfs",
        max_depth=3,
        max_visits=50,
    )

    before = glob.glob("./output/output*.png")
    _ = c.crawl()

    savedir = f"{os.getcwd()}/test"
    c.plot_topology(savedir)

    after = glob.glob("./output/output*.png")
    assert len(before) == len(after) -1


def test_fetch_page():
    c = Crawler(
        root="https://www.unipa.it",
        strategy="bfs",
        max_depth=3,
    )
    link = Link(c.root, 0)
    empty = Link("", 0)

    # malformed urls don't pass
    assert c._fetch_page(Link("https://unipa.it", 0))
    assert c._fetch_page(link)
    assert not c._fetch_page(Link("httpp://www.unipa.it", 1))
    assert not c._fetch_page(empty)


def test_fetch_article():
    c = Crawler(
        root="https://www.unipa.it",
        strategy="bfs",
        max_depth=3,
    )
    rettori = Link("https://www.unipa.it/ateneo/Storia-dellAteneo/index.html", 0)
    home = Link("https://www.unipa.it", 0)

    s1 = c._fetch_page(rettori)
    s2 = c._fetch_page(home)

    assert c._fetch_articles(s1) != ""
    assert c._fetch_articles(s2) == ""


def test_fetch_links():
    c = Crawler(
        root="https://www.unipa.it",
        strategy="bfs",
        max_depth=3,
    )
    soup = BeautifulSoup(c.root, "lxml")
    assert c._fetch_links(soup) != []


def test_dfs_step():
    first_level = ["1", "2", "3"]
    lvl2_1 = ["1a", "1b", "1c"]
    lvl2_2 = ["2a", "2b", "2c"]
    lvl2_3 = ["3a", "3b", "2c"]

    raise NotImplementedError


def test_bfs_step():
    first_level = ["1", "2", "3"]
    lvl2_1 = ["1a", "1b", "1c"]
    lvl2_2 = ["2a", "2b", "2c"]
    lvl2_3 = ["3a", "3b", "2c"]
    raise NotImplementedError


def test_remove_nonbreaking():
    assert "\xa0" not in remove_nonbreaking("ciao\xa0")
    assert "\xa0" not in remove_nonbreaking("ciao\xa0\xa0")
