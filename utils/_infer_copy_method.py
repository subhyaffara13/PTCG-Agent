
def _infer_copy_method(
    node: nodes.Call, context: InferenceContext | None = None, **kwargs: Any
) -> Iterator[CopyResult]:
    assert isinstance(node.func, nodes.Attribute)
    inferred_orig, inferred_copy = itertools.tee(node.func.expr.infer(context=context))
    if all(
        isinstance(
            inferred_node, (nodes.Dict, nodes.List, nodes.Set, objects.FrozenSet)
        )
        for inferred_node in inferred_orig
    ):
        return cast(Iterator[CopyResult], inferred_copy)

    raise UseInferenceDefault

