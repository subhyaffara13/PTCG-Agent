
def make_channels_last_2d_strides_for(
    shape: Sequence[_IntLikeT],
) -> tuple[_IntLikeT | int, ...]:
    # TODO: maybe inform the user of channels_last_3d if rank of the tensor is 5?
    torch._check(
        len(shape) == 4,
        lambda: "Only tensors of rank 4 can use the channels_last memory format",
    )

    multiplier: _IntLikeT | int = 1
    strides: list[_IntLikeT | int] = [0] * 4
    for idx in (1, -1, -2, 0):
        # NOTE: intentionally divergence from make_contiguous_strides_for
        # This is consistent with eager
        strides[idx] = multiplier
        multiplier *= shape[idx]

    return tuple(strides)

