
def get_fake_tensor_from_node_arg(
    node: torch.fx.node.Argument,
) -> torch.Tensor | None:
    if (
        not hasattr(node, "meta")
        or ("val" not in node.meta)  # type: ignore[union-attr]
        or not isinstance(node.meta["val"], torch.Tensor)  # type: ignore[union-attr]
    ):
        return None
    return node.meta["val"]  # type: ignore[union-attr]

