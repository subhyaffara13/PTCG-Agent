
def sample_inputs_addr(op_info, device, dtype, requires_grad, **kwargs):
    make_arg = partial(
        make_tensor, device=device, dtype=dtype, requires_grad=requires_grad, low=None, high=None
    )
    yield SampleInput(make_arg(S, M), make_arg(S), make_arg(M))

    yield SampleInput(make_arg(), make_arg(S), make_arg(M)).with_metadata(broadcasts_input=True)

    if dtype.is_complex:
        alpha, beta = 0.1 + 0.3j, 0.4 + 0.6j
    elif dtype.is_floating_point:
        alpha, beta = 0.2, 0.6
    else:
        alpha, beta = 2, 3

    yield SampleInput(make_arg(S, M), make_arg(S), make_arg(M), beta=beta, alpha=alpha)

    yield SampleInput(
        make_arg(),
        make_arg(S),
        make_arg(M),
        beta=beta,
        alpha=alpha,
    ).with_metadata(broadcasts_input=True)

    # These samples fail gradcheck
    if dtype.is_floating_point and not requires_grad:
        tensor_options = dict(device=device, dtype=dtype, requires_grad=requires_grad)
        yield SampleInput(
            torch.tensor([[math.nan]], **tensor_options),
            torch.tensor([0.0], **tensor_options),
            torch.tensor([0.0], **tensor_options),
            beta=0.0,
            alpha=0.0,
        ).with_metadata(broadcasts_input=True)

        yield SampleInput(
            torch.tensor([[0.0]], **tensor_options),
            torch.tensor([math.nan], **tensor_options),
            torch.tensor([math.nan], **tensor_options),
            beta=0.0,
            alpha=0.0,
        ).with_metadata(broadcasts_input=True)

