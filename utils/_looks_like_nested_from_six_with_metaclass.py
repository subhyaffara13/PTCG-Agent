
def _looks_like_nested_from_six_with_metaclass(node) -> bool:
    if len(node.bases) != 1:
        return False
    base = node.bases[0]
    if not isinstance(base, nodes.Call):
        return False
    try:
        if hasattr(base.func, "expr"):
            # format when explicit 'six.with_metaclass' is used
            mod = base.func.expr.name
            func = base.func.attrname
            func = f"{mod}.{func}"
        else:
            # format when 'with_metaclass' is used directly (local import from six)
            # check reference module to avoid 'with_metaclass' name clashes
            mod = base.parent.parent
            import_from = mod.locals["with_metaclass"][0]
            func = f"{import_from.modname}.{base.func.name}"
    except (AttributeError, KeyError, IndexError):
        return False
    return func == SIX_WITH_METACLASS

