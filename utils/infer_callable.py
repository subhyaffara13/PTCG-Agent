
def infer_callable(node, context: InferenceContext | None = None):
    """Understand callable calls.

    This follows Python's semantics, where an object
    is callable if it provides an attribute __call__,
    even though that attribute is something which can't be
    called.
    """
    if len(node.args) != 1:
        # Invalid callable call.
        raise UseInferenceDefault

    argument = node.args[0]
    try:
        inferred = next(argument.infer(context=context))
    except (InferenceError, StopIteration):
        return util.Uninferable
    if isinstance(inferred, util.UninferableBase):
        return util.Uninferable
    return nodes.Const(inferred.callable())

