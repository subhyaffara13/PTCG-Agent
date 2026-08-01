
def infer_typing_generic_class_pep695(
    node: nodes.ClassDef, ctx: context.InferenceContext | None = None
) -> Iterator[nodes.ClassDef]:
    """Add __class_getitem__ for generic classes. Python 3.12+."""
    func_to_add = _extract_single_node(CLASS_GETITEM_TEMPLATE)
    node.locals["__class_getitem__"] = [func_to_add]
    return iter([node])

