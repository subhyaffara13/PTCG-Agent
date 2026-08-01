
def countOf(a: Iterable[_T], b: _T, /) -> int:
    return sum(it is b or it == b for it in a)

