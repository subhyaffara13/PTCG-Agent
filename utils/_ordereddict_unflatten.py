
def _ordereddict_unflatten(
    values: Iterable[T],
    context: Context,
) -> OrderedDict[Any, T]:
    return OrderedDict((key, value) for key, value in zip(context, values, strict=True))

