
def set_getitem(s: set[T], n: int) -> T:
    # Set ordering might not be stable
    return list(s)[n]

