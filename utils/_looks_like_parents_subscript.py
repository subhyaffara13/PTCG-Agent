
def _looks_like_parents_subscript(node: nodes.Subscript) -> bool:
    if not (
        isinstance(node.value, nodes.Attribute) and node.value.attrname == "parents"
    ):
        return False

    try:
        value = next(node.value.infer())
    except (InferenceError, StopIteration):
        return False
    parents = "builtins.tuple" if PY313 else "pathlib._PathParents"
    return (
        isinstance(value, bases.Instance)
        and isinstance(value._proxied, nodes.ClassDef)
        and value.qname() == parents
    )

