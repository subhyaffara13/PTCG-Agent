
def _standard_normal(
    shape: Sequence[int | SymInt],
    dtype: _dtype | None,
    device: Device | None,
) -> Tensor:
    if torch._C._get_tracing_state():
        # [JIT WORKAROUND] lack of support for .normal_()
        return torch.normal(
            torch.zeros(shape, dtype=dtype, device=device),
            torch.ones(shape, dtype=dtype, device=device),
        )
    return torch.empty(shape, dtype=dtype, device=device).normal_()

