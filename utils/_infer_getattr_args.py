
def _infer_getattr_args(node, context):
    if len(node.args) not in (2, 3):
        # Not a valid getattr call.
        raise UseInferenceDefault

    try:
        obj = next(node.args[0].infer(context=context))
        attr = next(node.args[1].infer(context=context))
    except (InferenceError, StopIteration) as exc:
        raise UseInferenceDefault from exc

    if isinstance(obj, util.UninferableBase) or isinstance(attr, util.UninferableBase):
        # If one of the arguments is something we can't infer,
        # then also make the result of the getattr call something
        # which is unknown.
        return util.Uninferable, util.Uninferable

    is_string = isinstance(attr, nodes.Const) and isinstance(attr.value, str)
    if not is_string:
        raise UseInferenceDefault

    return obj, attr.value

