
def infer_dataclass_field_call(
    node: nodes.Call, ctx: context.InferenceContext | None = None
) -> Iterator[InferenceResult]:
    """Inference tip for dataclass field calls."""
    if not isinstance(node.parent, (nodes.AnnAssign, nodes.Assign)):
        raise UseInferenceDefault
    result = _get_field_default(node)
    if not result:
        yield Uninferable
    else:
        default_type, default = result
        if default_type == "default":
            yield from default.infer(context=ctx)
        else:
            new_call = parse(default.as_string()).body[0].value
            new_call.parent = node.parent
            yield from new_call.infer(context=ctx)

