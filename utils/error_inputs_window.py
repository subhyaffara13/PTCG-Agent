
def error_inputs_window(op_info, device, *args, **kwargs):
    # Tests for windows that have a negative size
    yield ErrorInput(
        SampleInput(-1, *args, dtype=torch.float32, device=device, **kwargs),
        error_type=ValueError,
        error_regex="requires non-negative window length, got M=-1",
    )

    # Tests for window tensors that are not torch.strided, for instance, torch.sparse_coo.
    yield ErrorInput(
        SampleInput(
            3,
            *args,
            layout=torch.sparse_coo,
            device=device,
            dtype=torch.float32,
            **kwargs,
        ),
        error_type=ValueError,
        error_regex="is implemented for strided tensors only, got: torch.sparse_coo",
    )

    # Tests for window tensors that are not floating point dtypes, for instance, torch.long.
    yield ErrorInput(
        SampleInput(3, *args, dtype=torch.long, device=device, **kwargs),
        error_type=ValueError,
        error_regex="expects float32 or float64 dtypes, got: torch.int64",
    )

    # Tests for window tensors that are bfloat16
    yield ErrorInput(
        SampleInput(3, *args, dtype=torch.bfloat16, device=device, **kwargs),
        error_type=ValueError,
        error_regex="expects float32 or float64 dtypes, got: torch.bfloat16",
    )

    # Tests for window tensors that are float16
    yield ErrorInput(
        SampleInput(3, *args, dtype=torch.float16, device=device, **kwargs),
        error_type=ValueError,
        error_regex="expects float32 or float64 dtypes, got: torch.float16",
    )

