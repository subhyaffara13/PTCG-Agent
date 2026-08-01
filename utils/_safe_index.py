
def _safe_index(lst: list, item: Any) -> int | None:
    """
    Helper function to find index of item in list.

    For DimEntry objects, uses __eq__ comparison which properly handles
    both positional and Dim entries.

    Returns the index if found, None if not found.
    """
    for i, list_item in enumerate(lst):
        # Use == for DimEntry objects as they have proper __eq__ implementation
        if isinstance(item, DimEntry) and isinstance(list_item, DimEntry):
            if list_item == item:
                return i
        elif list_item is item:
            return i
    return None

