
def _get_local_callable(
    node: nodes.NodeNG, attr: str
) -> tuple[CallableObjects | None, bool, bool]:
    try:
        c = node.local_attr(attr)[-1]
    except astroid.NotFoundError:
        c = None
    is_from_object = bool(c and c.parent.scope().name == "object")
    is_from_builtins = bool(c and c.root().name in sys.builtin_module_names)
    return c, is_from_object, is_from_builtins

