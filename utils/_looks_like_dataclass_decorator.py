
def _looks_like_dataclass_decorator(
    node: nodes.NodeNG, decorator_names: frozenset[str] = DATACLASSES_DECORATORS
) -> bool:
    """Return True if node looks like a dataclass decorator.

    Uses inference to lookup the value of the node, and if that fails,
    matches against specific names.
    """
    if isinstance(node, nodes.Call):  # decorator with arguments
        node = node.func
    try:
        inferred = next(node.infer())
    except (InferenceError, StopIteration):
        inferred = Uninferable

    if isinstance(inferred, UninferableBase):
        if isinstance(node, nodes.Name):
            return node.name in decorator_names
        if isinstance(node, nodes.Attribute):
            return node.attrname in decorator_names

        return False

    return (
        isinstance(inferred, nodes.FunctionDef)
        and inferred.name in decorator_names
        and inferred.root().name in DATACLASS_MODULES
    )

