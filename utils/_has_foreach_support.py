
def _has_foreach_support(tensors: list[Tensor], device: torch.device) -> bool:
    return _device_has_foreach_support(device) and all(
        t is None or type(t) in _foreach_supported_types for t in tensors
    )

