
def mark_as_skip_wait(x: ir.IRNode) -> None:
    """
    If a non-blocking collective is lowered as a blocking collective, the wait
    node in the original graph becomes useless and we can skip the lowering it.
    """
    _bufs_to_skip_wait.add((id(V.graph), x.get_name()))

