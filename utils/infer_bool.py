
def infer_bool(node, context: InferenceContext | None = None):
    """Understand bool calls."""
    if len(node.args) > 1:
        # Invalid bool call.
        raise UseInferenceDefault

    if not node.args:
        return nodes.Const(False)

    argument = node.args[0]
    try:
        inferred = next(argument.infer(context=context))
    except (InferenceError, StopIteration):
        return util.Uninferable
    if isinstance(inferred, util.UninferableBase):
        return util.Uninferable

    bool_value = inferred.bool_value(context=context)
    if isinstance(bool_value, util.UninferableBase):
        return util.Uninferable
    return nodes.Const(bool_value)

