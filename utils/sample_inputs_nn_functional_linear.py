
def sample_inputs_nn_functional_linear(op_info, device, dtype, requires_grad, **kwargs):
    for njt in _sample_njts(
        device=device, dtype=dtype, requires_grad=requires_grad, dims=[3, 4, 5]
    ):
        # projection over a ragged dim is not currently supported
        if is_nested_int(njt.size(-1)):
            continue

        # with bias
        NUM_OUTPUT = 10
        weight = torch.randn(
            NUM_OUTPUT,
            njt.size(-1),
            device=device,
            dtype=dtype,
            requires_grad=requires_grad,
        )
        bias = torch.randn(
            NUM_OUTPUT, device=device, dtype=dtype, requires_grad=requires_grad
        )
        yield SampleInput(
            _clone(njt),
            kwargs={
                "weight": _clone(weight),
                "bias": _clone(bias),
            },
            name=f"{_describe_njt(njt)}: with bias",
        )

        # without bias
        yield SampleInput(
            _clone(njt),
            kwargs={
                "weight": _clone(weight),
            },
            name=f"{_describe_njt(njt)}: without bias",
        )

