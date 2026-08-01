
def _is_target_name_in_binop_side(
    target: nodes.AssignName | nodes.AssignAttr, side: nodes.NodeNG | None
) -> bool:
    """Determine whether the target name-like node is referenced in the side node."""
    match (side, target):
        case [nodes.Name(), nodes.AssignName()]:
            return target.name == side.name  # type: ignore[no-any-return]
        case [nodes.Attribute(), nodes.AssignAttr()]:
            return target.as_string() == side.as_string()  # type: ignore[no-any-return]
        case [nodes.Subscript(), nodes.Subscript()]:
            return subscript_chain_is_equal(target, side)
        case _:
            return False

