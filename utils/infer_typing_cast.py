
def infer_typing_cast(
    node: nodes.Call, ctx: context.InferenceContext | None = None
) -> Iterator[nodes.NodeNG]:
    """Infer call to cast() returning same type as casted-from var."""
    if not isinstance(node.func, (nodes.Name, nodes.Attribute)):
        raise UseInferenceDefault

    try:
        func = next(node.func.infer(context=ctx))
    except (InferenceError, StopIteration) as exc:
        raise UseInferenceDefault from exc
    if not (
        isinstance(func, nodes.FunctionDef)
        and func.qname() == "typing.cast"
        and len(node.args) == 2
    ):
        raise UseInferenceDefault

    return node.args[1].infer(context=ctx)

