
def register_type(
    name: str, kind: type
) -> Callable[[Callable[[Any, ISortPrettyPrinter], str]], Callable[[Any, ISortPrettyPrinter], str]]:
    """Registers a new literal sort type."""

    def wrap(
        function: Callable[[Any, ISortPrettyPrinter], str],
    ) -> Callable[[Any, ISortPrettyPrinter], str]:
        type_mapping[name] = (kind, function)
        return function

    return wrap

