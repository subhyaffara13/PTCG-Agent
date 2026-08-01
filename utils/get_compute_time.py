
def get_compute_time(func_packet, args, kwargs, out, out_dtypes) -> float:  # type: ignore[no-untyped-def]
    """
    Estimates the compute time of an aten operator.

    Args:
        func_packet: The operator overload packet.
        args: The arguments to the operator.
        kwargs: The keyword arguments to the operator.
        out: The output of the operator.
        out_dtypes: The output data types.

    Returns:
        float: The estimated compute time in nanoseconds.
    """
    if func_packet in flop_registry:
        if len(out_dtypes) != 1:
            raise AssertionError(
                f"Only support single out dtype got {out_dtypes} for {func_packet}"
            )
        dtype = out_dtypes.pop()
        # This actually gives peta-FLOPs/s hence multiply by 1e15 to get the FLOPs/s
        peak_gpu_flops = get_device_tflops(dtype) * 1e15
        # We can expect to achieve 75% of theoretical peak flops
        factor = 0.75
        peak_empirical_flops = factor * peak_gpu_flops
        flop_count_func = flop_registry[func_packet]
        # We divide by a factor of 2 to get the MACs (multiply and accumulate)
        flop_count = flop_count_func(*args, **kwargs, out_val=out) / 2
        # We multiply by 1e9 to get the time in nano seconds
        compute_time = (flop_count / peak_empirical_flops) * 1e9
        return compute_time
    return 0.0

