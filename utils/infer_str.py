
def infer_str(node, context: InferenceContext | None = None) -> nodes.Const:
    """Infer str() calls.

    :param nodes.Call node: str() call to infer
    :param context.InferenceContext: node context
    :rtype nodes.Const: a Const containing an empty string
    """
    call = arguments.CallSite.from_call(node, context=context)
    if call.keyword_arguments:
        raise UseInferenceDefault("TypeError: str() must take no keyword arguments")
    try:
        return nodes.Const("")
    except (AstroidTypeError, InferenceError) as exc:
        raise UseInferenceDefault(str(exc)) from exc

