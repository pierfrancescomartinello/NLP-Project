import re
import json
#TODO Delete this file

#TODO Move this function into crawler.py
def remove_nonbreaking(text: str) -> str:
    return re.sub("(\xa0)+", " ", text)
