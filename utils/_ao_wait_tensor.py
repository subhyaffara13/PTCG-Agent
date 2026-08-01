
def _ao_wait_tensor(
    tensor: torch.Tensor,
    keepalive: torch.Tensor | None = None,
) -> torch.Tensor:
    completion_event, device = _pop_wait(tensor)
    current_stream = torch.accelerator.current_stream(device)
    current_stream.wait_event(completion_event)
    return tensor

