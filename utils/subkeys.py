
def subkeys(key: Key) -> Iterable[Key]:
    return [elt for elt in key if isinstance(elt, tuple)]

