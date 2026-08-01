
def device_sleep(device: str, cycles: int) -> None:
    """Sleep for the given number of cycles on the specified device.

    For CPU, temporarily patches torch.cpu._sleep if needed.
    For CUDA/other devices, uses torch.get_device_module(device)._sleep.
    """
    if device == "cpu":
        orig = getattr(torch.cpu, "_sleep", None)
        torch.cpu._sleep = _cpu_sleep
        try:
            torch.cpu._sleep(cycles)
        finally:
            if orig is None:
                delattr(torch.cpu, "_sleep")
            else:
                torch.cpu._sleep = orig
    else:
        torch.get_device_module(device)._sleep(cycles)

