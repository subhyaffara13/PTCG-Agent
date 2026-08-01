
def _get_tensor(node: torch.fx.Node) -> torch.Tensor:
    val = node.meta["val"]
    assert isinstance(val, torch.Tensor)
    return val

