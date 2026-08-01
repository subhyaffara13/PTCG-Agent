
def object_issubclass(
    node: nodes.NodeNG,
    class_or_seq: list[InferenceResult],
    context: InferenceContext | None = None,
) -> util.UninferableBase | bool:
    """Check if a type is a subclass of any node in class_or_seq.

    :raises AstroidTypeError: if the given ``classes_or_seq`` are not types
    :raises AstroidError: if the type of the given node cannot be inferred
        or its type's mro doesn't work
    """
    if not isinstance(node, nodes.ClassDef):
        raise TypeError(f"{node} needs to be a ClassDef node, not {type(node)!r}")
    return _object_type_is_subclass(node, class_or_seq, context=context)

