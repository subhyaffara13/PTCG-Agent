
def sample_inputs_softmax_variant(
    op_info,
    device,
    dtype,
    requires_grad,
    with_dtype=False,
    use_zero_dimensions=True,
    **kwargs,
):
    make_arg = partial(
        make_tensor, device=device, dtype=dtype, requires_grad=requires_grad
    )
    cases = [
        ((S,), (0,)),
        ((S, S), (0,)),
        ((S, S), (1,)),
        ((S, S), (-1,)),
        ((S, M, S), (2,)),
        *([((S, 0, 0), (-1,))] if use_zero_dimensions else []),
    ]
    kwargs = (
        dict(
            dtype=(
                torch.bfloat16 if torch.device(device).type == "mps" else torch.float64
            )
        )
        if with_dtype
        else None
    )

    # PyTorch on XLA throws an error when passed with dim argument for 0d tensor.
    # See https://github.com/pytorch/xla/issues/3061 for more details.
    if torch.device(device).type != "xla":
        cases.append(((), (0,)))

    return (
        SampleInput(make_arg(shape), args=dim, kwargs=kwargs) for shape, dim in cases
    )

