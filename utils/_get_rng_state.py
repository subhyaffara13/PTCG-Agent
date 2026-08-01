
def _get_rng_state() -> tuple[torch.Tensor, dict[int, torch.Tensor]]:
    """
    Gets CPU and accelerator (e.g., CUDA, XPU device) rng states from all devices.
    """
    return (torch.get_rng_state(), _collect_accelerator_rng_states())

