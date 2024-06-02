from typing import Callable
from bs4 import BeautifulSoup
import requests
from collections import namedtuple

from preprocessor import remove_linebreak

# Define a namedtuple for representing a hyperlink and its depth in the crawling process
Link = namedtuple("Link", ["addr", "depth"])


class Crawler:
    """
    A web crawler that explores links starting from a root URL up to a specified depth using a given strategy.

    Attributes:
    - max_depth (int): Maximum depth to which the crawler will follow links.
    - root (str): The root URL from which the crawling starts.
    - strategy (str): The strategy to use for crawling ("bfs" or "dfs").
    - _do_strategy (Callable): The method to execute the chosen crawling strategy.
    - _links (List[Link]): The list of links to be processed.
    - _visited (Set[str]): A set of URLs that have already been visited. We deal with URLs instead of their hashes due to the fact that Python does that under the hood.
    """

    max_depth: int
    root: str
    strategy: str
    _do_strategy: Callable
    _links: list[Link] = []
    _visited: set[str] = set()

    def __init__(self, root, max_depth, strategy="bfs"):
        """
        Initializes the Crawler with the root URL, maximum depth, and crawling strategy.

        Parameters:
        - root (str): The root URL to start crawling from.
        - max_depth (int): The maximum depth to crawl.
        - strategy (str): The crawling strategy ("bfs" for breadth-first search or "dfs" for depth-first search).
        """

        self.max_depth = max_depth
        self.root = root
        self.strategy = strategy
        self._links = [Link(root, 0)]  # Start with the root URL at depth 0
        self._visited = set()  # The visited set is initialized as empty

        # Dictionary mapping strategy names to their corresponding methods
        _funcs = {
            "dfs": self._dfs_step,
            "bfs": self._bfs_step,
        }

        # Assign the strategy method based on the chosen strategy
        self._do_strategy = lambda x, y, z: _funcs[self.strategy](x, y, z)

    def _bfs_step(self, x: list[Link], y: list[Link], depth: int):
        """
        Executes a single step of the breadth-first search (BFS) strategy.

        Parameters:
        - x (ist[Link]): The current list of links to be processed.
        - y (ist[str]): The new links found to be added to the list.
        - depth (int): The current depth of the crawl.

        Returns:
        - list[Link]: The updated list of links after performing BFS step.
        """
        y = [Link(el, depth + 1) for el in y]
        return x + y

    def _dfs_step(self, x: list[Link], y: list[Link], depth: int):
        """
        Executes a single step of the depth-first search (DFS) strategy.

        Parameters:
        - x (list[Link]): The current list of links to be processed.
        - y (list[str]): The new links found to be added to the list.
        - depth (int): The current depth of the crawl.

        Returns:
        - list[Link]: The updated list of links after performing DFS step.
        """
        y = [Link(el, depth + 1) for el in y]
        return y + x

    def _fetch_page(self, link: Link) -> BeautifulSoup:
        """
        Fetches the content of the page at the given link using an HTTP GET request.

        Parameters:
        - link (Link): The link to fetch the page from.

        Returns:
        - BeautifulSoup: The parsed content of the page.
        """
        res = requests.get(link.addr)
        return BeautifulSoup(res.content, "lxml")

    def _fetch_links(self, soup: BeautifulSoup) -> set[str]:
        """
        Extracts all hyperlinks from the given BeautifulSoup object.

        Parameters:
        - soup (BeautifulSoup): The parsed content of a web page.

        Returns:
        - set[str]: A set of URLs (as strings) found in the page.
        """
        return set(a["href"] for a in soup.find_all("a", href=True))

    def _fetch_articles(self, soup: BeautifulSoup) -> list[str]:
        """
        Extracts article texts from the given BeautifulSoup object.

        Parameters:
        - soup (BeautifulSoup): The parsed content of a web page.

        Returns:
        - list[str]: A list of article texts found in the page.
        """
        texts = []

        for art in soup.find_all("article"):
            paragraphs = art.find_all("p")

            text = "".join(remove_linebreak(p.get_text()) for p in paragraphs)
            texts.append(text)

        return texts

    def crawl(self) -> list[str]:
        """
        Starts the crawling process from the root URL, following links up to the maximum depth.

        Returns:
        - list[str]: A list of articles extracted from the crawled pages.
        """

        articles = []
        # Until we have finished crawling
        while self._links != []:
            # We pop the first element in the structure, LIFO or FIFO order depends by the strategy
            node = self._links.pop()
            # If the node has not been already visited, we visit it
            if node.addr not in self._visited:
                # Visualization and debug helper
                print(
                    f"\033[32m Depth: {node.depth}, Links: {len(self._links)}, Visited: {len(self._visited)} \033[0m"
                )

                # We flag the URL as visited
                self._visited.add(node.addr)

                # Starting analyzing the important text
                soup = self._fetch_page(node)
                articles += self._fetch_articles(soup)

                # If we have not reached the maximum depth, we explore the hyperlinks of the page
                if node.depth < self.max_depth:
                    neigh_links = self._fetch_links(soup)

                    # Cleaning links that are not useful to our crawling (non www.unipa.it sites) or already visited
                    neigh_links = _clean_links(self._visited, neigh_links)

                    # We add the new URLs to the structure
                    self._links = self._do_strategy(
                        self._links, neigh_links, node.depth
                    )
            else:
                # Visualization that helps in case we are visiting something already visited
                print("\033[31m Page already visited! \033[0m")

        return articles


def _clean_links(_visited: set[Link], links: set[str]) -> list[str]:
    """
    Cleans and filters the given set of links to include only those from the domain "://www.unipa.it"
    and excludes those that contain "://www.unipa.it/.". It also cleans the links from the site
    already visited

    Parameters:
    - _visited (set[str]): The set of URLs that have already been visited.
    - links (set[str]): The set of links to be cleaned.

    Returns:
    - list[str]: The cleaned list of links.
    """
    temp = set(
        [
            i
            for i in list(links)
            if "://www.unipa.it" in i and "://www.unipa.it/." not in i
        ]
    )
    return list(temp - _visited)


if __name__ == "__main__":
    c = Crawler(
        root="https://www.unipa.it",
        strategy="bfs",
        max_depth=3,
    )

    articles = c.crawl()
    print(articles)
