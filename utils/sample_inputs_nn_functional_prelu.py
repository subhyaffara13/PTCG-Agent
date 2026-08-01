
def sample_inputs_nn_functional_prelu(op_info, device, dtype, requires_grad, **kwargs):
    for njt in _sample_njts(
        device=device, dtype=dtype, requires_grad=requires_grad, dims=[3, 4]
    ):
        # Second dim is interpreted as number of channels; this should be non-ragged for now
        num_channels = njt.size(1)
        if is_nested_int(num_channels):
            continue

        # 1D weight
        weight = torch.randn(
            num_channels,
            device=device,
            dtype=dtype,
            requires_grad=requires_grad,
        )

        yield SampleInput(
            _clone(njt),
            kwargs={
                "weight": _clone(weight),
            },
            name=f"{_describe_njt(njt)}: 1D weight",
        )

        # scalar tensor weight
        yield SampleInput(
            _clone(njt),
            kwargs={
                "weight": torch.tensor(4.2, device=device, dtype=dtype),
            },
            name=f"{_describe_njt(njt)}: scalar tensor weight",
        )

