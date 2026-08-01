
def _calculate_transfer_size(device_put_node: fx.Node) -> int:
    """Calculate the size in bytes of data being transferred."""

    # ao.offload(tensor) -> tensor at args[0]
    # ao.reload(tensor, device) -> tensor at args[0]
    if device_put_node.target in (
        torch.ops.ao.offload.default,
        torch.ops.ao.reload.default,
    ):
        return _size_of(device_put_node.args[0])  # pyrefly: ignore [bad-argument-type]
    raise ValueError(f"Unexpected transfer op: {device_put_node.target}")

