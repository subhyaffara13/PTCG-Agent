
def norm_hash_fn(t: torch.Tensor, use_scalar: bool = False) -> torch.Tensor | float:
    """
    from Observer. Computes a hash for a tensor by converting it to float (if needed), making it contiguous,
    replacing NaN/inf values with fixed numbers, and then computing the L1 norm in float64 or complex128.
    This is used to generate a deterministic summary value for tensor comparison.
    """
    with torch._C._DisablePythonDispatcher():
        if not (t.is_floating_point() or t.is_complex()):
            t = t.float()
        t = t.contiguous()

        if t.is_complex():
            t_float = t.to(dtype=torch.complex128)
        else:
            t_float = t.to(dtype=torch.float64)

        out = t_float.norm(p=1)
        if use_scalar:
            return out.item()
        return out

