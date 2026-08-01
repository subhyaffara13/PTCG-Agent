
def suggest_memory_format(x: TensorLikeType) -> torch.memory_format:
    if x.layout != torch.strided:
        return torch.contiguous_format

    if are_strides_like_channels_last_or_false(x.shape, x.stride()):
        return torch.channels_last if x.ndim == 4 else torch.channels_last_3d

    return torch.contiguous_format

