
def rebuild_meta_tensor(
    tensor_cls,
    tensor_size,
    tensor_stride,
    tensor_offset,
    dtype,
    storage_size_bytes,
    requires_grad,
):
    untyped_storage = torch.UntypedStorage(storage_size_bytes, device="meta")

    typed_storage = torch.TypedStorage(
        wrap_storage=untyped_storage, dtype=dtype, _internal=True
    )

    t = torch._utils._rebuild_tensor(
        typed_storage,
        tensor_offset,
        tensor_size,
        tensor_stride,
    )

    if tensor_cls == torch.nn.parameter.Parameter:
        # It is crucial for integer tensors to receive
        # the requires_grad=False as an argument in the constructor
        t = torch.nn.parameter.Parameter(t, requires_grad=requires_grad)
    else:
        t.requires_grad = requires_grad

    return t

