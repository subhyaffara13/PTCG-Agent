
def repeat_interleave_Tensor(
    repeat: torch.Tensor,
    output_size: int | None = None,
) -> torch.Tensor:
    if config.triton.autotune_at_compile_time:
        # We can't compile-time auto-tune this because
        # it expects specific data in `repeat`
        return NotImplemented
    if output_size is None or type(output_size) is not int:
        return NotImplemented
    if repeat.device.type == "mps":
        return NotImplemented
    assert repeat.dtype in [torch.int32, torch.int64]
    assert repeat.ndim == 1
    cumsum = repeat.cumsum(0)
    pos = torch.arange(output_size, device=repeat.device)
    indices = torch.searchsorted(
        cumsum, pos, out_int32=(repeat.dtype == torch.int32), right=True
    )
    return torch.clamp(indices, max=repeat.size(0) - 1)

