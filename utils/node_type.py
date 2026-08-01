
def node_type(node: nodes.NodeNG) -> SuccessfulInferenceResult | None:
    """Return the inferred type for `node`.

    If there is more than one possible type, or if inferred type is Uninferable or None,
    return None
    """
    # check there is only one possible type for the assign node. Else we
    # don't handle it for now
    types: set[SuccessfulInferenceResult] = set()
    try:
        for var_type in node.infer():
            if isinstance(var_type, util.UninferableBase) or is_none(var_type):
                continue
            types.add(var_type)
            if len(types) > 1:
                return None
    except astroid.InferenceError:
        return None
    return types.pop() if types else None

