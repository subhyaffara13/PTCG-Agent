
def _ag_group_key_multidtype(node: torch.fx.Node) -> tuple[str]:
    _, group_size, group_name = node.args
    assert isinstance(group_name, str)
    return (group_name,)

