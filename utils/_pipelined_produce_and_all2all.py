
def _pipelined_produce_and_all2all(
    chunk_producer: Callable[[int, torch.Tensor], None],
    output: torch.Tensor,
    group_name: c10d.GroupName,
    out_chunk_dim: int = 0,
) -> None:
    """
    Perform the following logic with micro-pipelined computation and
    communication:

        chunks = [
            chunk_producer(dst_rank, chunks[dst_rank])
            for dst_rank in range(group_size):
        ]
        dist.all_to_all_single(output=output, input=torch.cat(chunks))
    """
    out_chunks = output.chunk(
        c10d._get_group_size_by_name(group_name), dim=out_chunk_dim
    )
    p2p_workspace_size_req = out_chunks[0].numel() * out_chunks[0].element_size() * 2
    symm_mem = get_symm_mem_workspace(group_name, min_size=p2p_workspace_size_req)
    group_size = symm_mem.world_size
    rank = symm_mem.rank

    symm_mem.barrier(channel=0)
    backend_stream = _get_backend_stream()
    backend_stream.wait_stream(torch.cuda.current_stream())

    def get_p2p_buf(rank: int, idx: int) -> torch.Tensor:
        if idx not in (0, 1):
            raise AssertionError
        offset = 0 if idx == 0 else out_chunks[0].numel()
        return symm_mem.get_buffer(
            rank, out_chunks[0].shape, out_chunks[0].dtype, offset
        )

    # Prepare two local p2p buffers, so that a remote rank can pull the result
    # of step [i] in one p2p buffer while the local rank can compute the
    # result of step [i+1] and write it directly the other p2p buffer.
    local_p2p_buf_0 = get_p2p_buf(rank, 0)
    local_p2p_buf_1 = get_p2p_buf(rank, 1)

    for step in range(1, group_size):
        remote_rank = (rank - step) % group_size
        if step % 2 == 0:
            stream = torch.cuda.current_stream()
            p2p_buf = local_p2p_buf_1
            remote_p2p_buf = get_p2p_buf(remote_rank, 1)
        else:
            stream = backend_stream
            p2p_buf = local_p2p_buf_0
            remote_p2p_buf = get_p2p_buf(remote_rank, 0)
        with stream:
            # Parallelization strategy: every rank issues independent compute
            # -> barrier -> p2p copy sequences on two streams. In addition to
            # computation/communication overlapping, the strategy allows for
            # computation/computation overlapping, greatly reducing
            # quantization inefficiency.
            #
            # Ideally, stream activities would look like this ("b" for
            # barriers, "cp" for p2p copies):
            #
            # [rank 0]
            # stream 0:         [  chunk_producer  ][b][ cp ][  chunk_producer ][b][ cp ]
            # stream 1: [  chunk_producer  ][b][ cp ][  chunk_producer  ][b][ cp ]
            #
            # [rank 1]
            # stream 0:         [  chunk_producer  ][b][ cp ][  chunk_producer ][b][ cp ]
            # stream 1: [  chunk_producer  ][b][ cp ][  chunk_producer  ][b][ cp ]
            #
            # Note that the barriers synchronize streams with the same ID
            # across ranks. They don't synchronize streams on the same rank.
            #
            # Since the work on both streams is independent, there's no
            # guarantee that the chunk_producer from stream 0 or stream 1 will
            # be scheduled first. If there is a scheduling mismatch across
            # ranks, the barrier forces all ranks to wait for the slowest.
            #
            # When scheduling mismatches occur among ranks, the stream
            # activities might look like this (note that p2p copies from
            # different streams cannot overlap with each other):
            #
            # [rank 0]
            # stream 0: [  chunk_producer  ][b        ][ cp ][  chunk_producer ][b       ][ cp ]
            # stream 1:         [  chunk_producer  ][b]      [ cp ][  chunk_producer  ][b]      [ cp ]
            #
            # [rank 1]
            # stream 0:         [  chunk_producer  ][b]      [ cp ][  chunk_producer  ][b]      [ cp ]
            # stream 1: [  chunk_producer  ][b        ][ cp ][  chunk_producer  ][b      ][ cp ]
            #
            # To prevent this, we need to ensure that the chunk_producer on
            # stream 1 gets scheduled first on every rank. Without access to
            # the underlying kernels, CUDA offers no API to control the
            # scheduling order of two independent, overlapping kernels. Our
            # solution is to issue a small sleep kernel in stream 0. The sleep
            # duration is insignificant, but having an extra task in stream 0
            # will almost guarantee that the chunk_producer on stream 1 gets
            # scheduled first. Once the first chunk_producer is scheduled in
            # the correct order, there's very little room for the scheduling
            # order of subsequent kernels to be inconsistent across ranks.
            if step == 2:
                torch.cuda._sleep(100)
            chunk_producer((rank + step) % group_size, p2p_buf)
            symm_mem.barrier(channel=step % 2)
            out_chunks[remote_rank].copy_(remote_p2p_buf)
            # The local P2P buffer can only be overwritten by the next
            # chunk_producer after all peers have finished reading from it.
            symm_mem.barrier(channel=step % 2)

    # If the sleep wasn't issued in the above loop, do it now.
    if group_size == 2:
        torch.cuda._sleep(100)

    chunk_producer(rank, out_chunks[rank])
    torch.cuda.current_stream().wait_stream(backend_stream)
    symm_mem.barrier(channel=0)

