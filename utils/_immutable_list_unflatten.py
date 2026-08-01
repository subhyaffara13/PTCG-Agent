
def _immutable_list_unflatten(
    values: Iterable[_T],
    context: Context,
) -> immutable_list[_T]:
    return immutable_list(_list_unflatten(values, context))

