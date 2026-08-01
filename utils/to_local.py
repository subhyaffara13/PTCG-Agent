
def to_local(t):
    """Unwrap a `DTensor` to its local shard if needed; pass through otherwise.

    Custom kernels (CUTLASS, CuteDSL, Triton) take raw tensor pointers and don't
    understand `DTensor`, so weights wrapped by FSDP2 / EP need this unwrap before
    they can be fed to the kernel. ``to_local()`` is autograd-aware on the train
    path: backward rewraps the gradient as a DTensor matching each parameter's
    placements.
    """
    if hasattr(torch.distributed, "tensor") and hasattr(torch.distributed.tensor, "DTensor"):
        if isinstance(t, torch.distributed.tensor.DTensor):
            return t.to_local()
    return t

