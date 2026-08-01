
def sample_inputs_i0_i1(op_info, device, dtype, requires_grad, **kwargs):
    exclude_zero = requires_grad and op_info.op is torch.special.i0e
    make_arg = partial(
        make_tensor,
        dtype=dtype,
        device=device,
        requires_grad=requires_grad,
        exclude_zero=exclude_zero,
    )
    yield SampleInput(make_arg((S,)))
    yield SampleInput(make_arg(()))

    if requires_grad and not exclude_zero:
        # Special Case for gradient
        # Sample with `0` in the input
        t = make_arg((S,))
        t[0] = 0

        yield SampleInput(t)

