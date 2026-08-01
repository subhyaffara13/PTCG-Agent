
def normalize_callback_names(callbacks: Iterable[Any]) -> List[Any]:
    if callbacks is None:
        return []
    return [c.lower() if isinstance(c, str) else c for c in callbacks]

