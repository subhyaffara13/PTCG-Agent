
def _infer_slice(node, context: InferenceContext | None = None):
    lower = _slice_value(node.lower, context)
    upper = _slice_value(node.upper, context)
    step = _slice_value(node.step, context)
    if all(elem is not _SLICE_SENTINEL for elem in (lower, upper, step)):
        return slice(lower, upper, step)

    raise AstroidTypeError(
        message="Could not infer slice used in subscript",
        node=node,
        index=node.parent,
        context=context,
    )

