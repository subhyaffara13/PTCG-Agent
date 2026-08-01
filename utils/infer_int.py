
def infer_int(node, context: InferenceContext | None = None):
    """Infer int() calls.

    :param nodes.Call node: int() call to infer
    :param context.InferenceContext: node context
    :rtype nodes.Const: a Const containing the integer value of the int() call
    """
    call = arguments.CallSite.from_call(node, context=context)
    if call.keyword_arguments:
        raise UseInferenceDefault("TypeError: int() must take no keyword arguments")

    if call.positional_arguments:
        try:
            first_value = next(call.positional_arguments[0].infer(context=context))
        except (InferenceError, StopIteration) as exc:
            raise UseInferenceDefault(str(exc)) from exc

        if isinstance(first_value, util.UninferableBase):
            raise UseInferenceDefault

        if isinstance(first_value, nodes.Const) and isinstance(
            first_value.value, (int, str)
        ):
            try:
                actual_value = int(first_value.value)
            except ValueError:
                return nodes.Const(0)
            return nodes.Const(actual_value)

    return nodes.Const(0)

