
def _looks_like_generic_class_pep695(node: nodes.ClassDef) -> bool:
    """Check if class is using type parameter. Python 3.12+."""
    return len(node.type_params) > 0

