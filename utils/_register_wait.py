
def _register_wait(tensor: torch.Tensor, device: torch.device) -> torch.Event:
    """Create an event for an async transfer and register it for wait_tensor."""
    event = torch.Event()
    _wait_registry[tensor.data_ptr()] = (event, device)
    return event

