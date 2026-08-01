
def _convert_to_params(
    tensors: list[torch.Tensor | nn.Parameter],
) -> list[nn.Parameter]:
    return [t if isinstance(t, nn.Parameter) else nn.Parameter(t) for t in tensors]

