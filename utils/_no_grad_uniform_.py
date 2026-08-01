
def _no_grad_uniform_(
    tensor: Tensor, a: float, b: float, generator: torch.Generator | None = None
) -> Tensor:
    with torch.no_grad():
        return tensor.uniform_(a, b, generator=generator)

