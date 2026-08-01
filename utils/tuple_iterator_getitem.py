
def tuple_iterator_getitem(it: Any, index: int) -> Any:
    _, (obj,), start = it.__reduce__()
    return obj[start + index]

