
def get_cls_type_hints(
    obj: type[Any],
    *,
    ns_resolver: NsResolver | None = None,
) -> dict[str, Any]:
    """Collect annotations from a class, including those from parent classes.

    Args:
        obj: The class to inspect.
        ns_resolver: A namespace resolver instance to use. Defaults to an empty instance.
    """
    hints: dict[str, Any] = {}
    ns_resolver = ns_resolver or NsResolver()

    for base in reversed(obj.__mro__):
        # For Python 3.14, we could also use `Format.VALUE` and pass the globals/locals
        # from the ns_resolver, but we want to be able to know which specific field failed
        # to evaluate:
        ann = safe_get_annotations(base)

        if not ann:
            continue

        with ns_resolver.push(base):
            globalns, localns = ns_resolver.types_namespace
            for name, value in ann.items():
                hints[name] = eval_type(value, globalns, localns)
    return hints

