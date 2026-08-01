
def _is_copy_node_bw_only(node: fx.Node) -> fx.Node | None:
    """Check if node is a view/reshape of a higher-order op output that aliases an input.

    Returns the original input node from the higher-order op's kwargs if the pattern
    matches, None otherwise.
    """
    if node.target not in (torch.ops.aten.view.default, torch.ops.aten.reshape.default):
        return None
    source = node.args[0]
    if not isinstance(source, fx.Node):
        return None
    return _get_ho_op_original_input(source)

