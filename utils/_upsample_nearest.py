
def _upsample_nearest(
    input: Tensor,
    output_size: list[int],
    scales: list[float | None],
    exact: bool = False,
) -> Tensor:
    spatial_indices = _compute_upsample_nearest_indices(
        input, output_size, scales, exact=exact
    )

    indices = [None, None] + spatial_indices
    result = aten._unsafe_index(input, indices)

    if result.ndim == 4:
        # convert output to correct memory format, if necessary
        memory_format = utils.suggest_memory_format(input)

        # following "heuristic: only use channels_last path when it's faster than the contiguous path"
        n_channels = input.shape[1]
        if input.device.type == "cuda" and n_channels < 4:
            memory_format = torch.contiguous_format

        result = result.contiguous(memory_format=memory_format)
    return result

