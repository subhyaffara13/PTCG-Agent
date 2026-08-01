
def get_transfer_time(flat_args_kwargs, flat_outs) -> float:  # type: ignore[no-untyped-def]
    """
    Estimates the memory transfer time of input and output tensors.

    Args:
        flat_args_kwargs (List[torch.Tensor]): The flat list of arguments and keyword arguments.
        flat_outs (List[torch.Tensor]): The flat list of outputs.

    Returns:
        float: The estimated memory transfer time in nanoseconds.
    """
    gpu_memory_bandwidth = get_gpu_dram_gbps()
    read_bytes = sum(
        get_num_bytes(t) for t in flat_args_kwargs if isinstance(t, torch.Tensor)
    )
    write_bytes = sum(
        get_num_bytes(t) for t in flat_outs if isinstance(t, torch.Tensor)
    )
    counted_bytes = read_bytes + write_bytes
    # The GPU memory bandwidth is in GB/s so the transfer time is in nanoseconds
    transfer_time = counted_bytes / gpu_memory_bandwidth
    return transfer_time

