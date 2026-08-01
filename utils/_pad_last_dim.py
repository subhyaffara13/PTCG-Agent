
def _pad_last_dim(
    tensor: torch.Tensor, alignment_size: int, slice: bool
) -> torch.Tensor:
    # FlashAttentionV2 requires that head dimension be a multiple of 8
    # This was previously done within the kernel, however
    # This causes the kernel to maybe alias query, key, value
    # So instead we pad the head_dimensions to be a multiple of 8
    # in the composite region
    last_dim_size = tensor.size(-1)
    if last_dim_size % alignment_size == 0:
        return tensor
    pad_count = alignment_size - (last_dim_size % alignment_size)
    tensor = torch.nn.functional.pad(tensor, [0, pad_count])
    if slice:
        return tensor[..., 0:last_dim_size]
    return tensor

