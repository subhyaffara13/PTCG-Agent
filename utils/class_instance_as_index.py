
def class_instance_as_index(node: bases.Instance) -> nodes.Const | None:
    """Get the value as an index for the given instance.

    If an instance provides an __index__ method, then it can
    be used in some scenarios where an integer is expected,
    for instance when multiplying or subscripting a list.
    """
    context = InferenceContext()
    try:
        for inferred in node.igetattr("__index__", context=context):
            if not isinstance(inferred, bases.BoundMethod):
                continue

            context.boundnode = node
            context.callcontext = CallContext(args=[], callee=inferred)
            for result in inferred.infer_call_result(node, context=context):
                if isinstance(result, nodes.Const) and isinstance(result.value, int):
                    return result
    except InferenceError:
        pass
    return None

