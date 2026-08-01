
def infer_getattr(node, context: InferenceContext | None = None):
    """Understand getattr calls.

    If one of the arguments is an Uninferable object, then the
    result will be an Uninferable object. Otherwise, the normal attribute
    lookup will be done.
    """
    obj, attr = _infer_getattr_args(node, context)
    if (
        isinstance(obj, util.UninferableBase)
        or isinstance(attr, util.UninferableBase)
        or not hasattr(obj, "igetattr")
    ):
        return util.Uninferable

    try:
        return next(obj.igetattr(attr, context=context))
    except (StopIteration, InferenceError, AttributeInferenceError):
        if len(node.args) == 3:
            # Try to infer the default and return it instead.
            try:
                return next(node.args[2].infer(context=context))
            except (StopIteration, InferenceError) as exc:
                raise UseInferenceDefault from exc

    raise UseInferenceDefault

