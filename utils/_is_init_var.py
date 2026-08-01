
def _is_init_var(node: nodes.NodeNG) -> bool:
    """Return True if node is an InitVar, with or without subscripting."""
    try:
        inferred = next(node.infer())
    except (InferenceError, StopIteration):
        return False

    return getattr(inferred, "name", "") == "InitVar"

