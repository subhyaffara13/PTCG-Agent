
def _ar_group_key(node: torch.fx.Node) -> tuple[str, str, torch.dtype]:
    _, reduce_op, group_name = node.args
    dtype = node.meta["val"].dtype
    assert isinstance(group_name, str)
    assert isinstance(reduce_op, str)
    return (group_name, reduce_op, dtype)

