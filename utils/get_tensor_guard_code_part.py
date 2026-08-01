
def get_tensor_guard_code_part(
    value: torch.Tensor,
    name: str,
    sizes: list[int | None],
    strides: list[int | None],
    pytype: type,
    dispatch_keys: DispatchKeySet,
) -> str:
    dispatch_key = (
        dispatch_keys | torch._C._dispatch_tls_local_include_set()
    ) - torch._C._dispatch_tls_local_exclude_set()
    dtype = value.dtype
    device_index = value.device.index
    requires_grad = value.requires_grad
    guard_str = (
        f"check_tensor({name}, {pytype.__qualname__}, {dispatch_key}, {dtype}, "
        f"device={device_index}, requires_grad={requires_grad}, size={sizes}, stride={strides})"
    )
    return guard_str

