import re

def get_protocol(url: str) -> str:
    url = stringify_path(url)
    parts = re.split(r"(\:\:|\://)", url, maxsplit=1)
    if len(parts) > 1:
        return parts[0]
    return "file"

