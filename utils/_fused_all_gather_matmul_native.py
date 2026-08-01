
def _fused_all_gather_matmul_native(
    A_shard: torch.Tensor,
    B: torch.Tensor,
    group_name: c10d.GroupName,
) -> tuple[torch.Tensor, torch.Tensor]:
    symm_mem = rendezvous(A_shard, group_name)
    if symm_mem is None:
        symm_mem = get_symm_mem_workspace(
            group_name, A_shard.numel() * A_shard.element_size()
        )
        symm_mem.barrier()
        buf = symm_mem.get_buffer(symm_mem.rank, A_shard.shape, A_shard.dtype)
        buf.copy_(A_shard)
        A_shard = buf

    rank = symm_mem.rank
    world_size = symm_mem.world_size

    current_stream = torch.cuda.current_stream()
    backend_stream = _get_backend_stream(priority=-1)

    symm_mem.barrier()
    backend_stream.wait_stream(current_stream)
    current_stream.wait_stream(backend_stream)

    A = A_shard.new_empty(A_shard.shape[0] * world_size, A_shard.shape[1])
    A_signals = torch.zeros(world_size, dtype=torch.uint32, device=A_shard.device)
    A_shards = A.chunk(world_size)

    A_shards[rank].copy_(A_shard)
    if not torch.cuda.is_current_stream_capturing():
        _SymmetricMemory.stream_write_value32(A_signals, rank, 1)
    else:
        _SymmetricMemory.memset32(A_signals, offset=rank, val=1, count=1)

    out = torch.ops.symm_mem._async_input_mm(A, B, A_signals, rank)
    for step in range(1, world_size):
        src_rank = (rank + step) % world_size
        src_buf = symm_mem.get_buffer(src_rank, A_shard.shape, A_shard.dtype)
        with backend_stream:
            A_shards[src_rank].copy_(src_buf)
            if not torch.cuda.is_current_stream_capturing():
                # cuStreamWriteValue32 issues a system level fence before the write
                _SymmetricMemory.stream_write_value32(A_signals, src_rank, 1)
            else:
                _SymmetricMemory.memset32(A_signals, offset=src_rank, val=1, count=1)

    current_stream.wait_stream(backend_stream)
    backend_stream.wait_stream(current_stream)

    symm_mem.barrier()
    return A, out

