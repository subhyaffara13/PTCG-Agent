
def _everyN(el, n):
    """Group the list el into groups of size n"""
    l = len(el)
    if l % n != 0:
        raise ValueError(el)
    for i in range(0, l, n):
        yield el[i : i + n]

