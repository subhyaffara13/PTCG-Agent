
def do_map(
    context: "Context",
    value: t.Union[t.AsyncIterable[t.Any], t.Iterable[t.Any]],
    name: str,
    *args: t.Any,
    **kwargs: t.Any,
) -> t.Iterable[t.Any]: ...


def do_map(
    context: "Context",
    value: t.Union[t.AsyncIterable[t.Any], t.Iterable[t.Any]],
    *,
    attribute: str = ...,
    default: t.Optional[t.Any] = None,
) -> t.Iterable[t.Any]: ...

