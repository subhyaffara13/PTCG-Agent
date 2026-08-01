
def _lerp_scalar(start: torch.Tensor, end: torch.Tensor, weight: float) -> torch.Tensor:
    # Decompose into sub + add(alpha=weight) so that the add lowering emits FMA,
    # matching eager CUDA's dual-formula (see aten/src/ATen/native/Lerp.h).
    # Convert end to start's memory format so the output preserves start's layout,
    # matching eager TensorIterator behavior.
    fmt = suggest_memory_format(start)
    if fmt != torch.contiguous_format:
        end = end.contiguous(memory_format=fmt)
    diff = end - start
    if weight >= 0.5 or weight <= -0.5:
        return torch.add(end, diff, alpha=-(1.0 - weight))
    return torch.add(start, diff, alpha=weight)

