import re

def _make_bookmark(s: str) -> str:
    """
    Converts a string into a valid HTML bookmark (ID or anchor name).
    """
    if s in _bookmark_lookup:
        return _bookmark_lookup[s]

    # Replace invalid characters with hyphens and ensure only valid characters
    bookmark = re.sub(r'[^a-zA-Z0-9-]+', '-', s)

    # Ensure it starts with a letter by adding 'z' if necessary
    if not bookmark[:1].isalpha():
        bookmark = f"z{bookmark}"

    # Convert to lowercase and strip hyphens
    bookmark = bookmark.lower().strip('-')

    _bookmark_lookup[s] = bookmark = f"{bookmark}-{next(_bookmark_ids):04d}"

    return bookmark

