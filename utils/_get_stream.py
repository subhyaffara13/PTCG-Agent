
def _get_stream(device: torch.device):
    """Get a background stream for copying between CPU and target device."""
    global _streams
    if device.type == "cpu" or not torch.accelerator.is_available():
        return None
    if torch.accelerator.current_accelerator().type != device.type:
        raise AssertionError(
            f"Expected current accelerator type {torch.accelerator.current_accelerator().type} "
            f"to match device type {device.type}"
        )
    if _streams is None:
        _streams = [None] * torch.accelerator.device_count()
    if _streams[device.index] is None:
        _streams[device.index] = torch.Stream(device.index)
    return _streams[device.index]

