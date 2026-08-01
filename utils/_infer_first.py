
def _infer_first(node, context):
    if isinstance(node, util.UninferableBase):
        raise UseInferenceDefault
    try:
        value = next(node.infer(context=context))
    except StopIteration as exc:
        raise InferenceError from exc
    if isinstance(value, util.UninferableBase):
        raise UseInferenceDefault()
    return value

