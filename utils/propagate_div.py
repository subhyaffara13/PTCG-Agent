
def propagate_div(div_node: Node) -> bool:
    lhs_node, rhs_node = div_node.args[:2]
    assert isinstance(lhs_node, Node)
    lhs_scale_by = get_scale_by_from_node(lhs_node)

    # When gradient accumulation is enabled, rhs_node can be a constant
    # representing the gradient accumulation steps
    rhs_scale_by = (
        get_scale_by_from_node(rhs_node) if isinstance(rhs_node, Node) else None
    )
    if lhs_scale_by and rhs_scale_by is None:
        update_chunking_meta(div_node, scale_by=lhs_scale_by)
        return True
    return False

