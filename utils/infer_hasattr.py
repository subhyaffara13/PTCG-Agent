
def infer_hasattr(node, context: InferenceContext | None = None):
    """Understand hasattr calls.

    This always guarantees three possible outcomes for calling
    hasattr: Const(False) when we are sure that the object
    doesn't have the intended attribute, Const(True) when
    we know that the object has the attribute and Uninferable
    when we are unsure of the outcome of the function call.
    """
    try:
        obj, attr = _infer_getattr_args(node, context)
        if (
            isinstance(obj, util.UninferableBase)
            or isinstance(attr, util.UninferableBase)
            or not hasattr(obj, "getattr")
        ):
            return util.Uninferable
        obj.getattr(attr, context=context)
    except UseInferenceDefault:
        # Can't infer something from this function call.
        return util.Uninferable
    except AttributeInferenceError:
        # Doesn't have it.
        return nodes.Const(False)
    return nodes.Const(True)

