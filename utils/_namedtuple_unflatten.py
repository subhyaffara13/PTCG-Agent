
def _namedtuple_unflatten(values: Iterable[T], context: Context) -> NamedTuple:
    return cast(NamedTuple, context(*values))

