
def ordered_unique(seq):
    """
    Return unique items in a sequence ``seq`` preserving their original order.
    """
    if not seq:
        return []
    uniques = []
    for item in seq:
        if item in uniques:
            continue
        uniques.append(item)
    return uniques


def ordered_unique(elements: Iterable[Any]) -> list[Any]:
    return list(collections.OrderedDict(dict.fromkeys(elements)).keys())

