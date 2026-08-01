
def torch_float(x):
    """
    Casts an input to a torch float32 tensor if we are in a tracing context, otherwise to a Python float.
    """
    if not _is_torch_available:
        return int(x)

    import torch

    return x.to(torch.float32) if torch.jit.is_tracing() and isinstance(x, torch.Tensor) else int(x)

