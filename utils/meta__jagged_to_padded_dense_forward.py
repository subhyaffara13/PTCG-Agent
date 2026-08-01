
def meta__jagged_to_padded_dense_forward(
    values: Tensor,
    offsets: list[Tensor],
    max_lengths: list[int],
    padding_value: float = 0.0,
):
    # only one jagged dim is supported for now
    if len(offsets) != 1:
        raise AssertionError(
            f"Only one jagged dim is supported, got {len(offsets)} offsets"
        )
    if len(max_lengths) != 1:
        raise AssertionError(
            f"Only one jagged dim is supported, got {len(max_lengths)} max_lengths"
        )

    B = offsets[0].shape[0] - 1
    S = max_lengths[0]
    output_shape = (B, S, *values.shape[1:])
    return values.new_empty(output_shape)

