
def is_channels_last_contiguous_or_false_3d(a: Tensor) -> bool:
    return is_channels_last_contiguous_3d(a, false_if_dde=True)

