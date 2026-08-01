
def bind_context_to_node(
    context: InferenceContext | None, node: SuccessfulInferenceResult
) -> InferenceContext:
    """Give a context a boundnode
    to retrieve the correct function name or attribute value
    with from further inference.

    Do not use an existing context since the boundnode could then
    be incorrectly propagated higher up in the call stack.
    """
    context = copy_context(context)
    context.boundnode = node
    return context

