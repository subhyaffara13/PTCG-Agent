
def _estimate_transfer_time_in_ms(transfer_size_bytes: int) -> float:
    """Estimate transfer time in milliseconds based on size and bandwidth.

    Uses config.activation_offload_cpu_gpu_bw (GB/s) which should be set by
    the user to match their hardware.
    """
    return (
        transfer_size_bytes / (1024**3) * 1_000 / config.activation_offload_cpu_gpu_bw
    )

