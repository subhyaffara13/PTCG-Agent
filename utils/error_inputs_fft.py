
def error_inputs_fft(op_info, device, **kwargs):
    make_arg = partial(make_tensor, device=device, dtype=torch.float32)
    # Zero-dimensional tensor has no dimension to take FFT of
    yield ErrorInput(
        SampleInput(make_arg()),
        error_type=IndexError,
        error_regex="Dimension specified as -1 but tensor has no dimensions",
    )

