
def _defaultdict_unflatten(
    values: Iterable[T],
    context: Context,
) -> defaultdict[Any, T]:
    default_factory, dict_context = context
    return defaultdict(default_factory, _dict_unflatten(values, dict_context))

