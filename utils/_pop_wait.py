
def _pop_wait(tensor: torch.Tensor) -> tuple[torch.Event, torch.device]:
    key = tensor.data_ptr()
    try:
        return _wait_registry.pop(key)
    except KeyError:
        raise RuntimeError(
            f"ao.wait_tensor: no pending transfer for tensor with data_ptr={key}. "
            "Every ao.wait_tensor must be paired with a preceding ao.offload or ao.reload."
        ) from None

