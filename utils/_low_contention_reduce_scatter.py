
def _low_contention_reduce_scatter(
    tensor: torch.Tensor,
    reduce_op: str,
    group_name: c10d.GroupName,
) -> torch.Tensor:
    """
    Performs reduce-scatter with symmetric memory in a low-contention fashion.

    This implementation performs a P2P-based all-to-all followed by an offline
    reduction.

    When `tensor` is already in symmetric memory:
        - Pull-based all-to-all is used.
        - No symmetric memory workspace is required.

    When `tensor` is not in symmetric memory:
        - Push-based all-to-all is used.
        - Symmetric memory workspace size requirement: the size of `tensor`.

    SM-usage:
        - SM-based copy of the rank's own chunk for the all-to-all.
        - Reduction on the all-to-all result.

    TODO(yifu): the SM-based copy can be avoided with a list-based reduction
    kernel.
    """
    symm_mem = rendezvous(tensor, group_name)
    if symm_mem is not None:
        return _low_contention_reduce_scatter_with_symm_mem_input(
            tensor, reduce_op, symm_mem
        )
    else:
        workspace = get_symm_mem_workspace(
            group_name, tensor.numel() * tensor.element_size()
        )
        return _low_contention_reduce_scatter_with_workspace(
            tensor, reduce_op, workspace
        )

