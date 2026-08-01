
def nsmallest(n, iterable, key=None):  # type: ignore[no-untyped-def]
    return py_heapq.nsmallest(n, iterable, key=key)

