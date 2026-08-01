
def _rebuild_device_tensor_from_cpu_tensor(data, dtype, device, requires_grad):
    device = _get_restore_location(device)
    tensor = data.to(dtype=dtype, device=device)
    tensor.requires_grad = requires_grad
    return tensor

