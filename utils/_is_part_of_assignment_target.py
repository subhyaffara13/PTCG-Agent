
def _is_part_of_assignment_target(node: nodes.NodeNG) -> bool:
    """Check whether use of a variable is happening as part of the left-hand
    side of an assignment.

    This requires recursive checking, because destructuring assignment can have
    arbitrarily nested tuples and lists to unpack.
    """
    match node.parent:
        case nodes.Assign():
            return node in node.parent.targets
        case nodes.AugAssign():
            return node == node.parent.target  # type: ignore[no-any-return]
        case nodes.Tuple() | nodes.List():
            return _is_part_of_assignment_target(node.parent)

    return False

