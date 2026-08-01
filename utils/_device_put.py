
def _device_put(x: TensorBox, device: torch.device, non_blocking=False):
    return to_device(x, device, copy=True, non_blocking=non_blocking)

