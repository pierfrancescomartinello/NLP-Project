from src.crawler import Crawler, fetch_page


def test_fetch_page():
    soup = fetch_page("https://ismyinternetworking.com/")
    assert soup.text


def test_set_strategy():
    c = Crawler(1, "https://ismyinternetworking.com/", "bfs")


def test_fetch_article():
    raise NotImplementedError


def test_fetch_links():
    raise NotImplementedError


def test_dfs():
    raise NotImplementedError


def test_bfs():
    raise NotImplementedError


def test_heuristic_search():
    raise NotImplementedError
