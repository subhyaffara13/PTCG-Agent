
def _decompress(state: LowPrecisionState, grad: torch.Tensor):
    """
    Casts gradients back to full parameter precision so that further computation happens in full precision.
    """
    orig_grad_data = grad.data
    grad.data = grad.data.to(state.parameter_type)
    device_type = ""
    try:
        if grad.device.type == "privateuse1":
            device_type = torch._C._get_privateuse1_backend_name()
        else:
            device_type = grad.device.type
        backend = getattr(torch, device_type)
    except AttributeError as e:
        raise AttributeError(
            f"Device {grad.device}  does not have a \
                corresponding backend registered as 'torch.device_type'."
        ) from e

    # Don't let this memory get reused until after the transfer.
    orig_grad_data.record_stream(backend.current_stream())  # type: ignore[arg-type]

