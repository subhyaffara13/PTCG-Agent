
def _collect_accelerator_rng_states() -> dict[int, torch.Tensor]:
    """
    Collects RNG state from all available acceleator devices.

    Returns:
        List of RNG state tensors, one for each accelerator device.
        Returns empty list if accelerator is not available.
    """
    if not torch.accelerator.is_available():
        return {}

    if torch.accelerator.is_available():
        device_idx = torch.accelerator.current_device_index()
        with torch.accelerator.device_index(device_idx):
            return {device_idx: torch.get_device_module().get_rng_state()}

    return {}

