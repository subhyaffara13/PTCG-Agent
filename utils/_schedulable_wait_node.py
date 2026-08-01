
def _schedulable_wait_node(node: torch.fx.Node) -> bool:
    """Check if this wait node is schedulable (waits on a recognized NCCL collective)."""
    return _get_collective_node_from_wait(node) is not None

