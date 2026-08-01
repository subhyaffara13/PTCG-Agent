
def hash_tensor_fn(t: torch.Tensor, use_scalar: bool = False) -> torch.Tensor | int:
    """
    wrapper over torch.hash_tensor
    """
    if isinstance(t, torch.distributed.tensor.DTensor):
        t = t.to_local()

    if t.is_floating_point():
        t_clean = t.to(dtype=torch.float64)
    elif t.is_complex():
        t_clean = t.to(dtype=torch.complex128).view(torch.float64)
    else:
        t_clean = t.to(dtype=torch.int64)

    if t.numel() > 0:
        out = torch.hash_tensor(t_clean)
    else:
        out = torch.zeros((), device=t_clean.device, dtype=torch.uint64)

    if use_scalar:
        return out.item()  # type: ignore[attribute]
    return out

