
def fuzzy_eq(x: bool | None, y: bool | None) -> bool | None:
    if None in (x, y):
        return None
    return x == y

