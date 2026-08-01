
def mesh_scatter(
    output: torch.Tensor,
    scatter_list: list[torch.Tensor],
    mesh: DeviceMesh,
    mesh_dim: int = 0,
    async_op: bool = False,
    *,
    group_src: int = 0,
) -> Work | None:
    """
    scatter a list of tensors to a device mesh dimension. We by default
    use the first rank of the mesh dimension as the source of truth, i.e
    for a 2d mesh [[0, 1], [2, 3]], if we scatter on mesh_dim = 1, we will
    scatter the tensor list on rank 0 to rank 0/1, and tensor list on rank
    2 to rank 2/3.

    Args:
        output (torch.Tensor): the tensor to receive the scattered list.
        scatter_list (List[torch.Tensor]): the tensor list to be scattered.
        mesh_dim (int, optional): indicate which mesh dimension we want
            to scatter on, we by default choose the first rank on the
            mesh dimension as source of truth.

    Keyword args:
        group_src (int, optional): the group rank of the source data for the
        logical/global tensor, on the specific mesh dimension. By default, we
        use ``group_rank=0`` on each DeviceMesh dimension as the source data
        to preserve the single-device semantic. If passing ``None`` explicitly,
        this method simply uses its local data with no communication.

    Returns:
        A :class:`Work` object
    """
    # TODO: Ideally we should use the meta tensor way
    # (to register a meta kernel for the collective op)
    # so that it would avoid the communication. Need to
    # remove the check below once that is done.
    if output.is_meta:
        return None
    dim_group = mesh.get_group(mesh_dim)
    if not isinstance(dim_group, ProcessGroup):
        raise AssertionError

    if group_src == get_rank(dim_group):
        fut = scatter(
            output,
            scatter_list=scatter_list,
            group=dim_group,
            async_op=async_op,
            group_src=group_src,
        )
    else:
        fut = scatter(
            output,
            scatter_list=None,
            group=dim_group,
            async_op=async_op,
            group_src=group_src,
        )

    return fut

