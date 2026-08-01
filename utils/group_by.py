
def group_by(items: Iterable[TItem], selector: Callable[[TItem], THash]) -> dict[THash, list[TItem]]:
    results = {}
    for item in items:
        key = selector(item)
        if key not in results:
            results[key] = []
        results[key].append(item)
    return results

