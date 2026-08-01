
def _rebuild_wrapper_subclass(
    cls,
    dtype,
    size,
    stride,
    storage_offset,
    layout,
    device,
    requires_grad,
):
    device = _get_restore_location(device)
    return torch.Tensor._make_wrapper_subclass(
        cls,
        size,
        strides=stride,
        dtype=dtype,
        storage_offset=storage_offset,
        layout=layout,
        device=device,
        requires_grad=requires_grad,
    )

