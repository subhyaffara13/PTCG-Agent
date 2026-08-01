
def memory_cached(device: "Device" = None) -> int:
    r"""Deprecated; see :func:`~torch.cuda.memory_reserved`."""
    return memory_reserved(device=device)

