
def _set_rng_state(
    cpu_state: torch.Tensor, accelerator_states: dict[int, torch.Tensor]
) -> None:
    """
    Sets CPU and accelerator (e.g., CUDA, XPU device) rng states for all devices. If
    the list of accelerator states is shorter than the number of devices only the
    first len(accelerator_states) devices will get their rng state set.
    """
    torch.set_rng_state(cpu_state)
    _set_accelerator_rng_states(accelerator_states)

