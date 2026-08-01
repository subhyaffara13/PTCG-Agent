
def make_channels_last_strides_for(
    shape: Sequence[_IntLikeT],
) -> tuple[_IntLikeT | int, ...]:
    ndim = len(shape) if isinstance(shape, Sequence) else 1
    if ndim == 3:
        return make_channels_last_1d_strides_for(shape)
    elif ndim == 4:
        return make_channels_last_2d_strides_for(shape)
    elif ndim == 5:
        return make_channels_last_3d_strides_for(shape)
    else:
        raise RuntimeError(
            f"no channels last format strides exist in {ndim} dimensions"
        )

