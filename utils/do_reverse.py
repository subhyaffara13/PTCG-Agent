
def do_reverse(value: str) -> str: ...


def do_reverse(value: "t.Iterable[V]") -> "t.Iterable[V]": ...


def do_reverse(value: t.Union[str, t.Iterable[V]]) -> t.Union[str, t.Iterable[V]]:
    """Reverse the object or return an iterator that iterates over it the other
    way round.
    """
    if isinstance(value, str):
        return value[::-1]

    try:
        return reversed(value)  # type: ignore
    except TypeError:
        try:
            rv = list(value)
            rv.reverse()
            return rv
        except TypeError as e:
            raise FilterArgumentError("argument must be iterable") from e

