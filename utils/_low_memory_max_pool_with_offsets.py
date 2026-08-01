
def _low_memory_max_pool_with_offsets(
    x,
    kernel_size,
    stride,
    padding,
    dilation,
    ceil_mode=False,
):
    n_dim = len(kernel_size)

    # assert we are not on a fallback path, the inductor decomp should have guaranteed this
    kernel_size, stride, padding, dilation, _ = max_pool_checks(
        x,
        kernel_size,
        stride,
        padding,
        dilation,
        n_dim,
        assert_fallback=False,
    )

    with config.patch(unroll_reductions_threshold=25):
        result, offsets = _max_pool_with_offsets(
            x,
            kernel_size,
            stride,
            padding,
            dilation,
            ceil_mode,
            n_dim=n_dim,
        )
        return result, to_dtype(offsets, torch.int8)

