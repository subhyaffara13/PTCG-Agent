
def _extract_register_target(dec: nodes.NodeNG) -> nodes.NodeNG | None:
    """
    If decorator `dec` looks like `@func.register(...)` or `@func.register`,
    return the `func` target node (Name or Attribute). Otherwise return None.
    """
    if isinstance(dec, nodes.Call):
        func_part = dec.func
        if isinstance(func_part, nodes.Attribute) and func_part.attrname == "register":
            return func_part.expr
        return None

    if isinstance(dec, nodes.Attribute) and dec.attrname == "register":
        return dec.expr

    return None

