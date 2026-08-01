
def infer_len(node, context: InferenceContext | None = None) -> nodes.Const:
    """Infer length calls.

    :param nodes.Call node: len call to infer
    :param context.InferenceContext: node context
    :rtype nodes.Const: a Const node with the inferred length, if possible
    """
    call = arguments.CallSite.from_call(node, context=context)
    if call.keyword_arguments:
        raise UseInferenceDefault("TypeError: len() must take no keyword arguments")
    if len(call.positional_arguments) != 1:
        raise UseInferenceDefault(
            "TypeError: len() must take exactly one argument "
            "({len}) given".format(len=len(call.positional_arguments))
        )
    [argument_node] = call.positional_arguments

    try:
        return nodes.Const(helpers.object_len(argument_node, context=context))
    except (AstroidTypeError, InferenceError) as exc:
        raise UseInferenceDefault(str(exc)) from exc

