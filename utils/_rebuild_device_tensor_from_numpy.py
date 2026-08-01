
def _rebuild_device_tensor_from_numpy(data, dtype, device, requires_grad):
    device = _get_restore_location(device)
    tensor = torch.from_numpy(data).to(dtype=dtype, device=device)
    tensor.requires_grad = requires_grad
    return tensor

