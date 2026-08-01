
def _class_or_tuple_to_container(
    node: InferenceResult, context: InferenceContext | None = None
) -> list[InferenceResult]:
    # Move inferences results into container
    # to simplify later logic
    # raises InferenceError if any of the inferences fall through
    try:
        node_infer = next(node.infer(context=context))
    except StopIteration as e:
        raise InferenceError(node=node, context=context) from e
    # arg2 MUST be a type or a TUPLE of types
    # for isinstance
    if isinstance(node_infer, nodes.Tuple):
        try:
            class_container = [
                next(node.infer(context=context)) for node in node_infer.elts
            ]
        except StopIteration as e:
            raise InferenceError(node=node, context=context) from e
    else:
        class_container = [node_infer]
    return class_container

