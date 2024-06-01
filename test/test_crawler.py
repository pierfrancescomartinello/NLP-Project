from src.crawler import fetch_page


def test_fetch_page():
    soup = fetch_page("https://ismyinternetworking.com/")
    assert soup.text
