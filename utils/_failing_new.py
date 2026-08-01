
def _failing_new(*args: t.Any, **kwargs: t.Any) -> "te.NoReturn":
    raise TypeError("can't create custom node types")

