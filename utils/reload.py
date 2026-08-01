
def reload(
    tensor: torch.Tensor,
    device: torch.device,
) -> torch.Tensor:
    """Async reload a CPU tensor to GPU on the dedicated transfer stream.

    The GPU tensor is allocated on the compute stream to avoid cross-stream
    allocator ownership issues. The H2D copy runs on the transfer stream.
    The completion event is keyed by the output tensor's data_ptr.
    """
    transfer_stream = _get_or_create_transfer_stream(device)
    current_stream = torch.accelerator.current_stream(device)

    # Allocate on compute stream so the allocator tracks ownership correctly
    result = torch.empty_like(tensor, device=device)
    completion_event = _register_wait(result, device)

    transfer_stream.wait_stream(current_stream)

    torch.accelerator.set_stream(transfer_stream)
    result.copy_(tensor, non_blocking=True)
    transfer_stream.record_event(completion_event)
    torch.accelerator.set_stream(current_stream)

    return result

