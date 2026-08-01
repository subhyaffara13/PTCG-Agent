
def infer_node(node: nodes.AssignAttr | nodes.AssignName) -> set[InferenceResult]:
    """Return a set containing the node annotation if it exists
    otherwise return a set of the inferred types using the NodeNG.infer method.
    """
    ann = get_annotation(node)
    try:
        if ann:
            if isinstance(ann, nodes.Subscript) or (
                isinstance(ann, nodes.BinOp) and ann.op == "|"
            ):
                return {ann}
            return set(ann.infer())
        return set(node.infer())
    except astroid.InferenceError:
        return {ann} if ann else set()

