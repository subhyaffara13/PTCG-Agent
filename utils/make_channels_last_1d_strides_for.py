
def make_channels_last_1d_strides_for(
    shape: Sequence[_IntLikeT],
) -> tuple[_IntLikeT | int, ...]:
    torch._check(
        len(shape) == 3,
        lambda: "Only tensors of rank 3 can use the channels_last_1d memory format",
    )

    multiplier: _IntLikeT | int = 1
    strides: list[_IntLikeT | int] = [0] * 3
    for idx in (1, -1, 0):
        # NOTE: intentionally divergence from make_contiguous_strides_for
        # This is consistent with eager
        strides[idx] = multiplier
        multiplier *= shape[idx]

    return tuple(strides)

