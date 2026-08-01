
def object_isinstance(
    node: InferenceResult,
    class_or_seq: list[InferenceResult],
    context: InferenceContext | None = None,
) -> util.UninferableBase | bool:
    """Check if a node 'isinstance' any node in class_or_seq.

    :raises AstroidTypeError: if the given ``classes_or_seq`` are not types
    """
    obj_type = object_type(node, context)
    if isinstance(obj_type, util.UninferableBase):
        return util.Uninferable
    return _object_type_is_subclass(obj_type, class_or_seq, context=context)

