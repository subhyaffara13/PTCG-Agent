
def select_or_reject(
    context: "Context",
    value: "t.Iterable[V]",
    args: t.Tuple[t.Any, ...],
    kwargs: t.Dict[str, t.Any],
    modfunc: t.Callable[[t.Any], t.Any],
    lookup_attr: bool,
) -> "t.Iterator[V]":
    if value:
        func = prepare_select_or_reject(context, args, kwargs, modfunc, lookup_attr)

        for item in value:
            if func(item):
                yield item

