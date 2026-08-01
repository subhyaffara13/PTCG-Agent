
def is_channels_last_contiguous_or_false(a: Tensor) -> bool:
    return is_channels_last_contiguous_or_false_2d(
        a
    ) or is_channels_last_contiguous_or_false_3d(a)

