
def zeros_and_scatter(
    shape: list[int],
    indices: list[Tensor],
    vals: Tensor,
) -> Tensor:
    """Custom Op so that we can register a custom lowering for the new_output + scatter in the backwards pass"""
    grad = torch.zeros(shape, device=vals.device, dtype=vals.dtype)
    return torch.ops.aten.index_put(grad, indices, vals, accumulate=True)

