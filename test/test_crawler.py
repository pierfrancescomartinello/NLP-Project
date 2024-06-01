from src.crawler import Crawler


def test_set_strategy():
    strategy = "bfs"

    c = Crawler(
        "https://ismyinternetworking.com/",
        1,
        strategy=strategy,
    )

    assert c.strategy == strategy


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
