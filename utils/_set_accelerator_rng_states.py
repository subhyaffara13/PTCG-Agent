
def _set_accelerator_rng_states(rng_states: dict[int, torch.Tensor]) -> None:
    """
    Sets RNG state for all accelerator devices from a list of states.

    Args:
        rng_states: List of RNG state tensors to restore.
    """
    if not torch.accelerator.is_available():
        return

    if torch.accelerator.is_available():
        for device_idx, device_rng_state in rng_states.items():
            with torch.accelerator.device_index(device_idx):
                torch.get_device_module().set_rng_state(device_rng_state)

