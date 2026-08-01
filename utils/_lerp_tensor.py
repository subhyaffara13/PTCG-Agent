
def _lerp_tensor(
    start: torch.Tensor, end: torch.Tensor, weight: torch.Tensor
) -> torch.Tensor:
    # Same dual-formula as foreach_lerp polyfill: decompose into sub + addcmul.
    # Convert end to start's memory format so the output preserves start's layout.
    fmt = suggest_memory_format(start)
    if fmt != torch.contiguous_format:
        end = end.contiguous(memory_format=fmt)
    diff = end - start
    mask = weight.abs() >= 0.5
    neg_omw = -(1.0 - weight)
    w = torch.where(mask, neg_omw, weight)
    base = torch.where(mask, end, start)
    return torch.addcmul(base, w, diff, value=1)

