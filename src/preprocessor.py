import re


def remove_nonbreaking(text: str) -> str:
    return re.sub("(\xa0)+", " ", text)
