
def _low_contention_reduce_scatter_with_workspace(
    tensor: torch.Tensor,
    reduce_op: str,
    workspace: _SymmetricMemory,
) -> torch.Tensor:
    rank = workspace.rank
    world_size = workspace.world_size

    if tensor.shape[0] % world_size != 0:
        raise AssertionError
    chunks = tensor.chunk(world_size)

    _get_backend_stream().wait_stream(torch.cuda.current_stream())
    with _get_backend_stream():
        # push + offline reduction
        workspace.barrier()
        for step in range(world_size):
            remote_rank = (rank - step) % world_size
            dst_buf = workspace.get_buffer(
                remote_rank, chunks[0].shape, chunks[0].dtype, chunks[0].numel() * rank
            )
            dst_buf.copy_(chunks[remote_rank])
        workspace.barrier()

        buf = workspace.get_buffer(rank, tensor.shape, tensor.dtype)
        ret = buf.unflatten(0, (world_size, -1))
        if reduce_op == "sum":
            ret = ret.sum(dim=0)
        elif reduce_op == "avg":
            ret = ret.mean(dim=0)
        else:
            raise ValueError(f"reduce_op ({reduce_op}) is not supported")
        torch._C._distributed_c10d._register_work(ret, Work())
        return ret

