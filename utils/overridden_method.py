
def overridden_method(
    klass: nodes.LocalsDictNodeNG, name: str | None
) -> nodes.FunctionDef | None:
    """Get overridden method if any."""
    try:
        parent = next(klass.local_attr_ancestors(name))
    except (StopIteration, KeyError):
        return None
    try:
        meth_node = parent[name]
    except KeyError:  # pragma: no cover
        # We have found an ancestor defining <name> but it's not in the local
        # dictionary. This may happen with astroid built from living objects.
        return None
    if isinstance(meth_node, nodes.FunctionDef):
        return meth_node
    return None  # pragma: no cover

