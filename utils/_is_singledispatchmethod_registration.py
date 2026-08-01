
def _is_singledispatchmethod_registration(node: nodes.FunctionDef) -> bool:
    """
    Return True if `node` is a function decorated like:

        @func.register(...)
        def _(…): ...

    where `func` is a singledispatchmethod (i.e. its base was decorated
    with @singledispatchmethod).
    """
    decorators = node.decorators
    if not decorators:
        return False

    for dec in decorators.nodes:
        target = _extract_register_target(dec)
        if target is None:
            continue

        if _inferred_has_singledispatchmethod(target):
            return True

    return False

