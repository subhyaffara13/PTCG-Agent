
def offload(tensor: torch.Tensor) -> torch.Tensor:
    """Async offload a GPU tensor to CPU on the dedicated transfer stream.

    Callers MUST pair this with an ``ao.wait_tensor`` that passes the source GPU
    tensor as ``keepalive`` to extend its lifetime past the async D2H copy.
    Do NOT use ``record_stream`` — it causes memory fragmentation and
    unbounded memory growth.

    Uses pinned-memory allocation + copy_ so the transfer is compatible
    with CUDA graph capture.
    """
    device = tensor.device
    transfer_stream = _get_or_create_transfer_stream(device)
    current_stream = torch.accelerator.current_stream(device)

    transfer_stream.wait_stream(current_stream)

    torch.accelerator.set_stream(transfer_stream)
    result = torch.empty_like(tensor, device="cpu", pin_memory=True)
    completion_event = _register_wait(result, device)
    result.copy_(tensor, non_blocking=True)
    transfer_stream.record_event(completion_event)
    torch.accelerator.set_stream(current_stream)

    return result

