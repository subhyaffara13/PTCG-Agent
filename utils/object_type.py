
def object_type(
    node: InferenceResult, context: InferenceContext | None = None
) -> InferenceResult | None:
    """Obtain the type of the given node.

    This is used to implement the ``type`` builtin, which means that it's
    used for inferring type calls, as well as used in a couple of other places
    in the inference.
    The node will be inferred first, so this function can support all
    sorts of objects, as long as they support inference.
    """

    try:
        types = set(_object_type(node, context))
    except InferenceError:
        return util.Uninferable
    if len(types) != 1:
        return util.Uninferable
    return next(iter(types))

