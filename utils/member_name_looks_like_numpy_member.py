
def member_name_looks_like_numpy_member(
    member_names: frozenset[str], node: nodes.Name
) -> bool:
    """
    Returns True if the Name node's name matches a member name from numpy
    """
    return node.name in member_names and node.root().name.startswith("numpy")

