
def _rebuild_meta_tensor_no_storage(dtype, size, stride, requires_grad):
    return torch.empty_strided(
        size, stride, dtype=dtype, device="meta", requires_grad=requires_grad
    )

