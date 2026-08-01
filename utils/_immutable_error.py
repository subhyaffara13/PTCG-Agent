
def _immutable_error(self: t.Any) -> t.NoReturn:
    raise TypeError(f"{type(self).__name__!r} objects are immutable")

