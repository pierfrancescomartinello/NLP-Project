import re


def remove_linebreak(text: str) -> str:
    return re.sub("(\xa0)+", "\n", text)
