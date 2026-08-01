
def native_layer_norm_default(func, *args, **kwargs):
    _, new_kwargs = normalize_function(  # type: ignore[misc]
        func, args=args, kwargs=kwargs, normalize_to_only_use_kwargs=True
    )

    inp = new_kwargs.pop("input")

    if inp.dim() <= 2:
        raise RuntimeError(
            "layer_norm(): not supported for NestedTensor objects with 2 or fewer dimensions"
        )

    normalized_shape = new_kwargs["normalized_shape"]
    ragged_size = inp.shape[inp._ragged_idx]

    num_dims_not_normalized = inp.dim() - len(normalized_shape)

    if (
        num_dims_not_normalized == 0
    ):  # error if trying to normalize over the batch dimension
        raise RuntimeError(
            "layer_norm(): not supported when normalizing over the batch dimension for NestedTensor"
        )

    if ragged_size in normalized_shape and inp._lengths is not None:
        raise RuntimeError(
            "layer_norm(): not supported where lengths is not None if operating on the ragged dimension for NestedTensor"
        )

    if (
        ragged_size in normalized_shape
    ):  # special handling for normalizing over the ragged dimension
        padded_input = torch.ops.aten._jagged_to_padded_dense_forward(
            inp._values.flatten(
                start_dim=inp._ragged_idx
            ),  # _jagged_to_padded_dense_forward requires values to be a 2D tensor
            [inp._offsets],
            max_lengths=[inp._max_seqlen],  # max length of ragged dimension
        )

        padded_mask = torch.ops.aten._jagged_to_padded_dense_forward(
            torch.ones((inp._values.shape[0], 1), device=inp.device, dtype=inp.dtype),
            [inp._offsets],
            max_lengths=[inp._max_seqlen],  # max length of ragged dimension
        ).expand(
            padded_input.shape
        )  # mask elements outside of the ragged dimension and expand to the same shape as padded input (3D dense tensor)

        ragged_lengths = (
            inp._offsets.diff().unsqueeze(1).unsqueeze(1) * padded_input.shape[2]
        )  # ragged dim * inner dim, since we sum over dims (1, 2) (the layer on which we normalize)

        mean = (
            torch.sum(
                padded_input,
                dim=(1, 2),
                keepdim=True,
            )
            / ragged_lengths
        )  # a sum over (1, 2) ensures layer norm, whereas a sum over (1) would be an instance norm

        padded_normalized = (
            (padded_input - mean) * padded_mask
        )  # mask elements outside of the ragged dimension size for correct variance calculation

        variance = (
            torch.sum(
                torch.square(padded_normalized),
                dim=(1, 2),
                keepdim=True,
            )
            / ragged_lengths
        )  # a sum over (1, 2) ensures layer norm, whereas a sum over (1) would be an instance norm

        std = torch.sqrt(variance + new_kwargs["eps"])
        padded_layer_norm = padded_normalized / std

        jagged_layer_norm_values = torch.ops.aten._padded_dense_to_jagged_forward(
            padded_layer_norm,
            [inp._offsets],
            total_L=inp._values.shape[
                0
            ],  # providing this parameter helps avoid a GPU/CPU sync
        ).unflatten(
            -1, inp.shape[inp._ragged_idx + 1 :]
        )  # unflatten last dimension back into original nested tensor shape, e.g. (B, *, WH) --> (B, *, W, H)

        return (
            NestedTensor(jagged_layer_norm_values, **extract_kwargs(inp)),
            mean,
            std,
        )

    output, mean, std = func(inp._values, **new_kwargs)
    return (NestedTensor(output, **extract_kwargs(inp)), mean, std)

