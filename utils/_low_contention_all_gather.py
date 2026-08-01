
def _low_contention_all_gather(
    tensor: torch.Tensor,
    group_name: c10d.GroupName,
) -> torch.Tensor:
    """
    Performs all-gather with symmetric memory in a low-contention fashion.

    When `tensor` is already in symmetric memory:
        - The collective is carried out without using SMs.
        - No symmetric memory workspace is required.

    When `tensor` is not in symmetric memory:
        - An extra SM-based copy is performed to copy the input data into the
          symmetric memory workspace.
        - Symmetric memory workspace size requirement: the size of `tensor`.
    """
    symm_mem = rendezvous(tensor, group_name)
    if symm_mem is not None:
        input_is_symm_mem = True
    else:
        symm_mem = get_symm_mem_workspace(
            group_name, tensor.numel() * tensor.element_size()
        )
        input_is_symm_mem = False

    rank = symm_mem.rank
    world_size = symm_mem.world_size

    output = tensor.new_empty(tensor.shape[0] * world_size, *tensor.shape[1:])
    chunks = output.chunk(world_size)

    _get_backend_stream().wait_stream(torch.cuda.current_stream())
    with _get_backend_stream():
        if not input_is_symm_mem:
            local_buf = symm_mem.get_buffer(rank, tensor.shape, tensor.dtype)
            local_buf.copy_(tensor)
        # pull
        symm_mem.barrier()
        for step in range(world_size):
            remote_rank = (rank - step) % world_size
            src_buf = symm_mem.get_buffer(remote_rank, tensor.shape, tensor.dtype)
            chunks[remote_rank].copy_(src_buf)
        symm_mem.barrier()
        torch._C._distributed_c10d._register_work(output, Work())
        return output

