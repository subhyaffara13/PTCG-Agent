
def _flipDict(d: dict[K, V]) -> dict[V, K]:
    flipped = {}
    for key, value in list(d.items()):
        flipped[value] = key
    return flipped

