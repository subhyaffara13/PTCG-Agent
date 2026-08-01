
def _graph_contains_triton_kernel_wrappers(gm: GraphModule) -> bool:
    """
    Check if the graph contains triton kernel wrapper nodes. These nodes contain
    references to the kernel_side_table which is process-local and can't be
    serialized across processes.
    """
    from torch._higher_order_ops.triton_kernel_wrap import (
        triton_kernel_wrapper_functional,
        triton_kernel_wrapper_mutation,
    )

    for module in gm.modules():
        if not isinstance(module, torch.fx.GraphModule):
            continue
        for node in module.graph.nodes:
            if node.target in (
                triton_kernel_wrapper_functional,
                triton_kernel_wrapper_mutation,
            ):
                return True
    return False

