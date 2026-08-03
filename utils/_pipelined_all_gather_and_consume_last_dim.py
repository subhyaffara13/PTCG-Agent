from typing import Callable

def _pipelined_all_gather_and_consume_last_dim(
    shard: torch.Tensor,
    shard_consumer: Callable[[torch.Tensor, int], None],
    ag_out: torch.Tensor,
    group_name: c10d.GroupName,
    ag_out_needed: bool = True,
) -> None:
    p2p_workspace_size_req = 0
    p2p_workspace_size_req = shard.numel() * shard.element_size()
    symm_mem = get_symm_mem_workspace(group_name, min_size=p2p_workspace_size_req)
    group_size = symm_mem.world_size
    rank = symm_mem.rank

    symm_mem.barrier(channel=0)
    backend_stream = _get_backend_stream()
    backend_stream.wait_stream(torch.cuda.current_stream())

    def copy_shard(dst: torch.Tensor, src: torch.Tensor) -> None:
        dst.copy_(src)

    def get_p2p_buf(remote_rank: int) -> torch.Tensor:
        buf = symm_mem.get_buffer(
            remote_rank,
            shard.shape,
            shard.dtype,
        )
        return buf

    local_p2p_buf = get_p2p_buf(rank)

    shards = ag_out.chunk(group_size)

    copy_shard(dst=local_p2p_buf, src=shard)
    symm_mem.barrier(channel=1)
    backend_stream.wait_stream(torch.cuda.current_stream())

    # At this point, all ranks have copied their local shard to
    # their local p2p buffer. Each rank can now copy and consume
    # remote shards.
    shard_consumer(shard, rank)

    for step in range(1, group_size):
        if step % 2 == 0:
            stream = torch.cuda.current_stream()
        else:
            stream = backend_stream
        remote_rank = (step + rank) % group_size
        remote_p2p_buf = get_p2p_buf(remote_rank)
        with stream:
            copy_shard(dst=shards[remote_rank], src=remote_p2p_buf)
            shard_consumer(shards[remote_rank], remote_rank)

    if ag_out_needed:
        # Copy from input to the all-gather output. Opportunistically overlap
        # it with the last shard_consumer.
        if group_size % 2 == 0:
            stream = torch.cuda.current_stream()
        else:
            stream = backend_stream
        with stream:
            copy_shard(dst=shards[rank], src=shard)

    torch.cuda.current_stream().wait_stream(backend_stream)
    symm_mem.barrier(channel=0)

