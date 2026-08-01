
def infer_dataclass_attribute(
    node: nodes.Unknown, ctx: context.InferenceContext | None = None
) -> Iterator[InferenceResult]:
    """Inference tip for an Unknown node that was dynamically generated to
    represent a dataclass attribute.

    In the case that a default value is provided, that is inferred first.
    Then, an Instance of the annotated class is yielded.
    """
    assign = node.parent
    if not isinstance(assign, nodes.AnnAssign):
        yield Uninferable
        return

    annotation, value = assign.annotation, assign.value
    if value is not None:
        yield from value.infer(context=ctx)
    if annotation is not None:
        yield from _infer_instance_from_annotation(annotation, ctx=ctx)
    else:
        yield Uninferable

