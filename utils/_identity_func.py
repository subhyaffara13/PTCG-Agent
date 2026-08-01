
def _identity_func(
    obj: torch.Tensor,
    pg: dist.ProcessGroup | None,
    device: torch.device | None,
    companion_obj: Any,
) -> torch.Tensor:
    return obj

