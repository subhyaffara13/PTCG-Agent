
def copy_slices_prologue(
    inputs: Sequence[torch.Tensor],
    base_sizes: Sequence[IntLikeType],
    base_strides: Sequence[IntLikeType],
    base_storage_offset: IntLikeType,
    view_sizes: Sequence[IntLikeType],
    view_strides: Sequence[IntLikeType],
    view_storage_offset: IntLikeType,
) -> list[torch.Tensor]:
    grad = inputs[0]
    result = grad.new_empty_strided(base_sizes, base_strides)
    assert grad is not None
    result.copy_(grad)
    offset = view_storage_offset - base_storage_offset
    grad_slice = result.as_strided(view_sizes, view_strides, offset)
    return [result, grad_slice, grad_slice.clone(memory_format=torch.contiguous_format)]

