
def propagate_add_sub(out_node: Node) -> bool:
    """
    The scale_by node of the two arguments must be the same.
    """
    lhs_node, rhs_node = get_args_of_node_type(out_node)
    assert isinstance(lhs_node, Node)
    assert isinstance(rhs_node, Node)
    lhs_meta, rhs_meta = get_chunking_metas([lhs_node, rhs_node])
    assert lhs_meta is not None
    assert rhs_meta is not None
    if lhs_meta.scale_by is rhs_meta.scale_by:
        update_chunking_meta(out_node, scale_by=lhs_meta.scale_by)
        return True
    return False

