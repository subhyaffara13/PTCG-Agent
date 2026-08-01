
def sync_do_first(
    environment: "Environment", seq: "t.Iterable[V]"
) -> "t.Union[V, Undefined]":
    """Return the first item of a sequence."""
    try:
        return next(iter(seq))
    except StopIteration:
        return environment.undefined("No first item, sequence was empty.")

