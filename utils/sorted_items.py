from typing import Any

def sorted_items(dictionary: dict[str, Any]) -> Iterator[tuple[str, Any]]:
    keys = sorted(dictionary.keys())
    for k in keys:
        yield k, dictionary[k]

