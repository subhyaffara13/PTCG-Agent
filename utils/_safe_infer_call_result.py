
def _safe_infer_call_result(
    node: nodes.FunctionDef,
    caller: nodes.FunctionDef,
    context: InferenceContext | None = None,
) -> InferenceResult | None:
    """Safely infer the return value of a function.

    Returns None if inference failed or if there is some ambiguity (more than
    one node has been inferred). Otherwise, returns inferred value.
    """
    try:
        inferit = node.infer_call_result(caller, context=context)
        value = next(inferit)
    except astroid.InferenceError:
        return None  # inference failed
    except StopIteration:
        return None  # no values inferred
    try:
        next(inferit)
        return None  # there is ambiguity on the inferred node
    except astroid.InferenceError:
        return None  # there is some kind of ambiguity
    except StopIteration:
        return value

