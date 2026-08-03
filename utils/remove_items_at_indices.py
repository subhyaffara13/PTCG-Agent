from typing import Any, List, Optional

def remove_items_at_indices(items: Optional[List[Any]], indices: Iterable[int]) -> None:
    """Remove items from a list in-place by index"""
    if items is None:
        return
    for index in sorted(set(indices), reverse=True):
        if 0 <= index < len(items):
            items.pop(index)

