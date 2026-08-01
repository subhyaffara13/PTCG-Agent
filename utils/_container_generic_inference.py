
def _container_generic_inference(
    node: nodes.Call,
    context: InferenceContext | None,
    node_type: type[nodes.BaseContainer],
    transform: Callable[[SuccessfulInferenceResult], nodes.BaseContainer | None],
) -> nodes.BaseContainer:
    args = node.args
    if not args:
        return node_type(
            lineno=node.lineno,
            col_offset=node.col_offset,
            parent=node.parent,
            end_lineno=node.end_lineno,
            end_col_offset=node.end_col_offset,
        )
    if len(node.args) > 1:
        raise UseInferenceDefault()

    (arg,) = args
    transformed = transform(arg)
    if not transformed:
        try:
            inferred = next(arg.infer(context=context))
        except (InferenceError, StopIteration) as exc:
            raise UseInferenceDefault from exc
        if isinstance(inferred, util.UninferableBase):
            raise UseInferenceDefault
        transformed = transform(inferred)
    if not transformed or isinstance(transformed, util.UninferableBase):
        raise UseInferenceDefault
    return transformed

