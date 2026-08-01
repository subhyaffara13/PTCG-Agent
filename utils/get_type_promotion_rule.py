
def get_type_promotion_rule(
    node: torch.fx.Node,
    type_promotion_table: TypePromotionTable,
) -> TypePromotionRule | None:
    """Get type promotion rule for a node.

    Args:
        node: Node to get type promotion rule for.
        type_promotion_table: Type promotion table.

    Returns:
        Type promotion rule for the node. None if no rule is found or if the node is not
        representing a torch operator.
    """
    op = node.target
    if not isinstance(op, torch._ops.OpOverload):
        return None
    if (rule := type_promotion_table.get_rule(op.overloadpacket)) is None:
        return None

    return rule

