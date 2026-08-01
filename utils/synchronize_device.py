
def synchronize_device(device_type: str, device_index: int) -> None:
    torch.accelerator.synchronize(torch.device(device_type, device_index))

