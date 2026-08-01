
def prepare_select_or_reject(
    context: "Context",
    args: t.Tuple[t.Any, ...],
    kwargs: t.Dict[str, t.Any],
    modfunc: t.Callable[[t.Any], t.Any],
    lookup_attr: bool,
) -> t.Callable[[t.Any], t.Any]:
    if lookup_attr:
        try:
            attr = args[0]
        except LookupError:
            raise FilterArgumentError("Missing parameter for attribute name") from None

        transfunc = make_attrgetter(context.environment, attr)
        off = 1
    else:
        off = 0

        def transfunc(x: V) -> V:
            return x

    try:
        name = args[off]
        args = args[1 + off :]

        def func(item: t.Any) -> t.Any:
            return context.environment.call_test(name, item, args, kwargs, context)

    except LookupError:
        func = bool  # type: ignore

    return lambda item: modfunc(func(transfunc(item)))

