
def _batched_linear(
    input: torch.Tensor,
    weight: torch.Tensor,
    bias: torch.Tensor | None = None,
    is_transposed: bool = False,
) -> torch.Tensor:
    """Batched linear layer supporting optional bias and transposed weights.

    Args:
        input (`torch.Tensor`):
            Input tensor of shape (batch_size, input_dim).
        weight (`torch.Tensor`):
            Weight tensor of shape (batch_size, output_dim, input_dim) if transposed is `False`,
            else of shape (batch_size, input_dim, output_dim).
        bias (`torch.Tensor`, *optional*):
            Bias tensor of shape (batch_size, output_dim). Default is `None`.
        is_transposed (`bool`, *optional*, defaults to `False`):
            Whether the weight tensor is transposed.
    Returns:
        `torch.Tensor`: Output tensor of shape (batch_size, output_dim).
    """
    if is_transposed:
        # (batch_size, 1, input_dim) @ (batch_size, input_dim, output_dim) -> (batch_size, 1, output_dim) -> (batch_size, output_dim)
        out = torch.bmm(input.unsqueeze(1), weight).squeeze(1)
    else:
        # (batch_size, output_dim, input_dim) @ (batch_size, input_dim, 1) -> (batch_size, output_dim, 1) -> (batch_size, output_dim)
        out = torch.bmm(weight, input.unsqueeze(-1)).squeeze(-1)

    if bias is not None:
        out.add_(bias)

    return out

