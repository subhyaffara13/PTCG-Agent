
def _low_contention_reduce_scatter_with_symm_mem_input(
    tensor: torch.Tensor,
    reduce_op: str,
    symm_mem: _SymmetricMemory,
) -> torch.Tensor:
    rank = symm_mem.rank
    world_size = symm_mem.world_size

    if tensor.shape[0] % world_size != 0:
        raise AssertionError
    a2a_res = torch.empty_like(tensor)
    chunks = a2a_res.chunk(world_size)

    _get_backend_stream().wait_stream(torch.cuda.current_stream())
    with _get_backend_stream():
        # pull + offline reduction
        symm_mem.barrier()
        for step in range(world_size):
            remote_rank = (rank - step) % world_size
            src_buf = symm_mem.get_buffer(
                remote_rank,
                chunks[0].shape,
                chunks[0].dtype,
                chunks[0].numel() * rank,
            )
            chunks[remote_rank].copy_(src_buf)
        symm_mem.barrier()

        ret = a2a_res.unflatten(0, (world_size, -1))
        if reduce_op == "sum":
            ret = ret.sum(dim=0)
        elif reduce_op == "avg":
            ret = ret.mean(dim=0)
        else:
            raise ValueError(f"reduce_op ({reduce_op}) is not supported")
        torch._C._distributed_c10d._register_work(ret, Work())
        return ret

