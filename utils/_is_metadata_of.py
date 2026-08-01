
def _is_metadata_of(group: Node, parent_group: Node) -> bool:
    """Check if a given group is a metadata group for a given parent_group."""
    if group._v_depth <= parent_group._v_depth:
        return False

    current = group
    while current._v_depth > 1:
        parent = current._v_parent
        if parent == parent_group and current._v_name == "meta":
            return True
        current = current._v_parent
    return False

