import math
from pathlib import Path
import requests
from typing import Callable
import json

import matplotlib.pyplot as plt
import networkx as nx
from bs4 import BeautifulSoup
import os
import validators
from collections import namedtuple

from preprocessor import remove_nonbreaking


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
    - _links (list[Link]): The list of links to be processed.
    - _visited (set[str]): A set of URLs that have already been visited. We deal with URLs instead of their hashes due to the fact that Python does that under the hood.
    """

    max_depth: int
    root: str
    strategy: str
    topology: nx.Graph
    _max_visits: int
    _do_strategy: Callable
    _links: list[Link] = []
    _visited: set[str] = set()

    def __init__(self, root, max_depth, max_visits=math.inf, strategy="bfs"):
        """
        Initializes the Crawler with the root URL, maximum depth, and crawling strategy.

        Parameters:
        - root (str): The root URL to start crawling from.
        - max_depth (int): The maximum depth to crawl.
        - strategy (str): The crawling strategy ("bfs" for breadth-first search or "dfs" for depth-first search).
        """

        self.max_depth = max_depth
        self.max_visits = max_visits
        self.root = root
        self.strategy = strategy
        self.topology = nx.Graph()
        self._links = [Link(root, 0)]  # Start with the root URL at depth 0
        self._visited = set()  # The visited set is initialized as empty
        self._articles = {}

        # Dictionary mapping strategy names to their corresponding methods
        _funcs = {
            "dfs": self._dfs_step,
            "bfs": self._bfs_step,
        }

        # Assign the strategy method based on the chosen strategy
        self._do_strategy = _funcs[self.strategy]

    def _bfs_step(self, queue: list[Link], nodes: list[str], depth: int):
        """
        Executes a single step of the breadth-first search (BFS) strategy.

        Parameters:
        - x (list[Link]): The current list of links to be processed.
        - y (list[Link]): The new links found to be added to the list.
        - depth (int): The current depth of the crawl.

        Returns:
        - list[Link]: The updated list of links after performing BFS step.
        """
        nodes = [Link(el, depth + 1) for el in nodes]
        return queue + nodes

    def _dfs_step(self, stack: list[Link], nodes: list[str], depth: int):
        """
        Executes a single step of the depth-first search (DFS) strategy.

        Parameters:
        - x (list[Link]): The current list of links to be processed.
        - y (list[str]): The new links found to be added to the list.
        - depth (int): The current depth of the crawl.

        Returns:
        - list[Link]: The updated list of links after performing DFS step.
        """
        nodes = [Link(el, depth + 1) for el in nodes]
        return nodes + stack

    def _fetch_page(self, link: Link) -> BeautifulSoup | None:
        """
        Fetches the content of the page at the given link using an HTTP GET request.

        Parameters:
        - link (Link): The link to fetch the page from.

        Returns:
        - BeautifulSoup: The parsed content of the page.
        """
        if not validators.url(link.addr):
            return None

        res = requests.get(link.addr)

        if res.ok:
            return BeautifulSoup(res.content, "lxml")

        print(f"Request to {link.addr} encountered an error.")
        return None

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

        for article in soup.find_all("article"):
            paragraphs = article.find_all("p")

            text = "".join(remove_nonbreaking(p.get_text()) for p in paragraphs)
            texts.append(text)

        return texts

    def plot_topology(self, destination: str = os.getcwd()):
        # Only the root has a visible label
        labels = {n: (n if n == self.root else "") for n in self.topology.nodes}

        # Draw a graph using matplotlib and networkx
        fig = plt.figure()
        nx.draw_kamada_kawai(
            self.topology,
            with_labels=True,
            node_size=10,
            font_size=7,
            edge_color="#847d7d",
            labels=labels,
        )

        # Saving it in memory
        fig.savefig(f"{destination}/topology.png")

    def crawl(self) -> dict[str, list[str]]:
        """
        Starts the crawling process from the root URL, following links up to the maximum depth.

        Returns:
        - list[str]: A list of articles extracted from the crawled pages.
        """

        # Until we have finished crawling
        while self._links != []:
            # We pop the first element in the structure, LIFO or FIFO order depends by the strategy
            node = self._links.pop()
            self.topology.add_node(node.addr)

            # Visit node if unvisited
            if node.addr in self._visited:
                print("\033[31m Page already visited! \033[0m")
                continue

            # Visualization and debug helper
            print(
                f"\033[32m Depth: {node.depth}, Links: {len(self._links)}, Visited: {len(self._visited)} \033[0m"
            )

            # We flag the URL as visited
            self._visited.add(node.addr)
            if len(self._visited) == self.max_visits:
                break

            # Starting analyzing the important text
            if (soup := self._fetch_page(node)) is None:
                continue

            self._articles[node.addr] = self._fetch_articles(soup)

            # If we have not reached the maximum depth, we explore the hyperlinks of the page
            if node.depth < self.max_depth:
                neigh_links = self._fetch_links(soup)

                # Cleaning links that are not useful to our crawling (non www.unipa.it sites) or already visited
                neigh_links = _clean_links(self._visited, neigh_links)

                for link in neigh_links:
                    self.topology.add_edge(node.addr, link)

                # We add the new URLs to the structure
                self._links = self._do_strategy(self._links, neigh_links, node.depth)

    def output_articles(self, output_dir: Path):
        with open(output_dir, "w", encoding="utf-8") as output:
            json.dump(self._articles, output, ensure_ascii=False)


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
            addr
            for addr in list(links)
            if "://www.unipa.it" in addr
            and "://www.unipa.it/.content" not in addr
            and not addr.endswith("pdf")
        ]
    )
    return list(temp - _visited)


if __name__ == "__main__":
    c = Crawler(
        root="https://www.unipa.it/",
        strategy="bfs",
        max_depth=3,
        max_visits=10,
    )

    c.crawl()
    c.output_articles("./output.json")

    c.plot_topology()
