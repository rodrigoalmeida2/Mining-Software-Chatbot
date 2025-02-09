import select
import sys
import re


def extract_owner_repo(url: str):
    pattern = r'https?://github.com/([^/]+)/([^/]+)'
    match = re.match(pattern, url)
    if match:
        owner, repo = match.groups()
        return owner, repo
    else:
        return None, None


def input_available():
    return select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], [])