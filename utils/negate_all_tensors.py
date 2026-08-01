
def negate_all_tensors(
    tensors: list[tuple[str, torch.Tensor]],
) -> list[tuple[str, torch.Tensor]]:
    """Return a new list with all tensors negated."""
    return [(name, -t) for name, t in tensors]

