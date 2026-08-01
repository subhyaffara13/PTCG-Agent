
def transpose_linear(
    input: torch.Tensor, weight: torch.Tensor, bias: torch.Tensor | None
) -> torch.Tensor:
    if bias is None:
        return torch.matmul(input.transpose(-1, -2), weight.t())
    return torch.matmul(input.transpose(-1, -2), weight.t()) + bias

