
def sample_inputs_nn_functional_rms_norm(
    op_info, device, dtype, requires_grad, **kwargs
):
    for njt in _sample_njts(
        device=device, dtype=dtype, requires_grad=requires_grad, dims=[3, 4]
    ):
        # normalize over non-ragged dims
        for start_dim in range(njt.dim()):
            if start_dim <= njt._ragged_idx:
                continue

            normalized_shape = njt.shape[start_dim:]
            weight = torch.randn(
                normalized_shape,
                device=device,
                dtype=dtype,
                requires_grad=requires_grad,
            )

            yield SampleInput(
                _clone(njt),
                kwargs={
                    "normalized_shape": normalized_shape,
                    "weight": weight,
                },
                name=f"{_describe_njt(njt)}",
            )

