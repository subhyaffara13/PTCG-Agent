
def _to_other(
    other: Tensor,
    non_blocking: bool = False,
    copy: bool = False,
    memory_format: torch.memory_format | None = None,
) -> dict[str, Any]:
    device = other.device
    dtype = other.dtype
    layout = other.layout
    # is_pinned issue #84925
    # pin_memory = other.is_pinned()
    kwargs = {
        "device": device,
        "dtype": dtype,
        "layout": layout,
        "non_blocking": non_blocking,
        "copy": copy,
        "memory_format": memory_format,
    }
    return kwargs

