
def _ag_group_key(node: torch.fx.Node) -> tuple[str, torch.dtype]:  # type: ignore[name-defined]
    _, group_size, group_name = node.args
    dtype = node.meta["val"].dtype
    assert isinstance(group_name, str)
    return (group_name, dtype)

