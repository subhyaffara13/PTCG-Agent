
def _ordereddict_flatten(d: OrderedDict[Any, T]) -> tuple[list[T], Context]:
    return list(d.values()), list(d.keys())

