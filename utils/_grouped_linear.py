
def _grouped_linear(
    input: torch.Tensor,
    weight: torch.Tensor,
    offs: torch.Tensor,
    bias: torch.Tensor | None = None,
    is_transposed: bool = False,
) -> torch.Tensor:
    """Grouped linear layer supporting optional bias and transposed weights.

    Args:
        input (`torch.Tensor`):
            Input tensor of shape (S, input_dim).
        weight (`torch.Tensor`):
            Weight tensor of shape (num_experts, input_dim, output_dim) if `is_transposed`,
            else of shape (num_experts, output_dim, input_dim).
        offs (`torch.Tensor`):
            Offsets tensor indicating the boundaries of each group in the input tensor.
        bias (`torch.Tensor`, *optional*):
            Bias tensor of shape (num_experts, output_dim). Default is `None`.
        is_transposed (`bool`, *optional*, defaults to `False`):
            Whether the weight tensor is transposed.
    Returns:
        `torch.Tensor`: Output tensor of shape (S, output_dim).
    """
    if is_transposed:
        # (S, input_dim) @ grouped (num_experts, input_dim, output_dim) -> (S, output_dim)
        out = _grouped_mm(input, weight, offs=offs)
    else:
        # (S, input_dim) @ grouped (num_experts, output_dim, input_dim).T -> (S, output_dim)
        out = _grouped_mm(input, weight.transpose(-2, -1), offs=offs)

    if bias is not None:
        # We should be able to pass bias to the grouped_mm call, but it's not yet supported.
        out.add_(bias)

    return out

