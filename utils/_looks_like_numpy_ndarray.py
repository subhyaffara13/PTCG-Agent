
def _looks_like_numpy_ndarray(node: nodes.Attribute) -> bool:
    return node.attrname == "ndarray"

