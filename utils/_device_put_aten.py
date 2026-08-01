
def _device_put_aten(
    a: Tensor, device: str | torch.device, non_blocking=False
) -> Tensor:
    return a.to(device, non_blocking=non_blocking)

