
def sample_inputs_window(op_info, device, dtype, requires_grad, *args, **kwargs):
    r"""Base function used to create sample inputs for windows.

    For additional required args you should use *args, as well as **kwargs for
    additional keyword arguments.
    """

    # Remove include_conjugated_inputs from kwargs
    kwargs.pop("include_conjugated_inputs", None)
    # Tests window sizes up to 5 samples.
    for size, sym in product(range(6), (True, False)):
        yield SampleInput(
            size,
            *args,
            sym=sym,
            device=device,
            dtype=dtype,
            requires_grad=requires_grad,
            **kwargs,
        )

