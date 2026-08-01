
def prepare_map(
    context: "Context", args: t.Tuple[t.Any, ...], kwargs: t.Dict[str, t.Any]
) -> t.Callable[[t.Any], t.Any]:
    if not args and "attribute" in kwargs:
        attribute = kwargs.pop("attribute")
        default = kwargs.pop("default", None)

        if kwargs:
            raise FilterArgumentError(
                f"Unexpected keyword argument {next(iter(kwargs))!r}"
            )

        func = make_attrgetter(context.environment, attribute, default=default)
    else:
        try:
            name = args[0]
            args = args[1:]
        except LookupError:
            raise FilterArgumentError("map requires a filter argument") from None

        def func(item: t.Any) -> t.Any:
            return context.environment.call_filter(
                name, item, args, kwargs, context=context
            )

    return func

