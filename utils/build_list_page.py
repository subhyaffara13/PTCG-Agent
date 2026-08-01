
def build_list_page(items: List[Any], has_more: bool = False) -> Dict[str, Any]:
    """Build the OpenAI-style paginated list response shape used by managed
    file/batch/vector-store listings. ``first_id`` and ``last_id`` are
    sourced from each item's ``.id`` attribute."""
    return {
        "object": "list",
        "data": items,
        "first_id": items[0].id if items else None,
        "last_id": items[-1].id if items else None,
        "has_more": has_more,
    }

