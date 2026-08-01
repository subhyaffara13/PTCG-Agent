
def _supports_protocol_method(value: nodes.NodeNG, attr: str) -> bool:
    try:
        attributes = value.getattr(attr)
    except astroid.NotFoundError:
        return False

    first = attributes[0]

    # Return False if a constant is assigned
    if isinstance(first, nodes.AssignName):
        this_assign_parent = get_node_first_ancestor_of_type(
            first, (nodes.Assign, nodes.NamedExpr)
        )
        if this_assign_parent is None:  # pragma: no cover
            # Cannot imagine this being None, but return True to avoid false positives
            return True
        if isinstance(this_assign_parent.value, nodes.BaseContainer):
            if all(isinstance(n, nodes.Const) for n in this_assign_parent.value.elts):
                return False
        if isinstance(this_assign_parent.value, nodes.Const):
            return False
    return True

