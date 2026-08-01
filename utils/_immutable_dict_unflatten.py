
def _immutable_dict_unflatten(
    values: Iterable[_VT],
    context: Context,
) -> immutable_dict[Any, _VT]:
    return immutable_dict(_dict_unflatten(values, context))

