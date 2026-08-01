
def sample_inputs_fft_with_min(
    op_info, device, dtype, requires_grad=False, *, min_size, **kwargs
):
    yield from sample_inputs_spectral_ops(
        op_info, device, dtype, requires_grad, **kwargs
    )
    if TEST_WITH_ROCM:
        # FIXME: Causes floating point exception on ROCm
        return

    # Check the "Invalid number of data points" error isn't too strict
    # https://github.com/pytorch/pytorch/pull/109083
    a = make_tensor(min_size, dtype=dtype, device=device, requires_grad=requires_grad)
    yield SampleInput(a)

