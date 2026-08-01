
def wait_tensor(tensor):
    """
    Wait on a tensor returned by the collectives ops.

    Waiting follows device semantics, which means blocking on CPU and synchronizing streams on CUDA.
    """
    return torch.ops._c10d_functional.wait_tensor(tensor)  # type: ignore[attr-defined]


def wait_tensor(
    tensor: torch.Tensor,
    keepalive: torch.Tensor | None = None,
) -> torch.Tensor:
    """Callable wrapper so ``wait_tensor`` can be imported by name for op registration."""
    return torch.ops.ao.wait_tensor.default(tensor, keepalive)

