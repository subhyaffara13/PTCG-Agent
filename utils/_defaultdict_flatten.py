
def _defaultdict_flatten(d: defaultdict[Any, T]) -> tuple[list[T], Context]:
    values, dict_context = _dict_flatten(d)
    return values, [d.default_factory, dict_context]

