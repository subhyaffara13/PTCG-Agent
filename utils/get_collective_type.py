
def get_collective_type(node: ir.IRNode) -> NCCL_COLL:
    if not isinstance(node, ir._CollectiveKernel):
        raise ValueError(f"node is not a collective kernel: {node}")

    name = node.python_kernel_name
    assert name is not None
    return get_collective_type_from_kernel_name(name)


def get_collective_type(node: torch.fx.Node) -> str:
    """Get the collective type name for a node."""
    if is_all_gather_into_tensor(node):
        return "all_gather"
    elif is_reduce_scatter_tensor(node):
        return "reduce_scatter"
    elif is_all_reduce_tensor(node):
        return "all_reduce"
    return ""

