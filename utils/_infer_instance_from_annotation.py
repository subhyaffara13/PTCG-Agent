
def _infer_instance_from_annotation(
    node: nodes.NodeNG, ctx: context.InferenceContext | None = None
) -> Iterator[UninferableBase | bases.Instance]:
    """Infer an instance corresponding to the type annotation represented by node.

    Currently has limited support for the typing module.
    """
    klass = None
    try:
        klass = next(node.infer(context=ctx))
    except (InferenceError, StopIteration):
        yield Uninferable
    if not isinstance(klass, nodes.ClassDef):
        yield Uninferable
    elif klass.root().name in {
        "typing",
        "_collections_abc",
        "",
    }:  # "" because of synthetic nodes in brain_typing.py
        if klass.name in _INFERABLE_TYPING_TYPES:
            yield klass.instantiate_class()
        else:
            yield Uninferable
    else:
        yield klass.instantiate_class()

