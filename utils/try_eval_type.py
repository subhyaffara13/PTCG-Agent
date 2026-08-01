
def try_eval_type(
    value: Any,
    globalns: GlobalsNamespace | None = None,
    localns: MappingNamespace | None = None,
) -> tuple[Any, bool]:
    """Try evaluating the annotation using the provided namespaces.

    Args:
        value: The value to evaluate. If `None`, it will be replaced by `type[None]`. If an instance
            of `str`, it will be converted to a `ForwardRef`.
        localns: The global namespace to use during annotation evaluation.
        globalns: The local namespace to use during annotation evaluation.

    Returns:
        A two-tuple containing the possibly evaluated type and a boolean indicating
            whether the evaluation succeeded or not.
    """
    value = _type_convert(value)

    try:
        return eval_type_backport(value, globalns, localns), True
    except NameError:
        return value, False

