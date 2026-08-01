
def filterfalse(function: _Predicate[_T], iterable: Iterable[_T], /) -> Iterator[_T]:
    it = iter(iterable)
    if function is None:
        return filter(operator.not_, it)
    else:
        return filter(lambda x: not function(x), it)

