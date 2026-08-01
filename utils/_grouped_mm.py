
def _grouped_mm(
    input: torch.Tensor,
    weight: torch.Tensor,
    offs: torch.Tensor,
) -> torch.Tensor:
    """Grouped matrix multiplication dispatcher that uses torch.nn.functional.grouped_mm if available, else falls back to torch._grouped_mm.

    Args:
        input (`torch.Tensor`):
            Input tensor of shape (S, input_dim).
        weight (`torch.Tensor`):
            Weight tensor of shape (num_experts, input_dim, output_dim).
        offs (`torch.Tensor`):
            Offsets tensor indicating the boundaries of each group in the input tensor.
    Returns:
        `torch.Tensor`: Output tensor of shape (S, output_dim).
    """

    if _can_use_grouped_mm(input, weight, offs):
        # torch.nn.functional.grouped_mm and torch._grouped_mm are not autocast-enabled,
        # when autocast is enabled we can end up with intermediate tensors in fp32 (e.g. LayerNorm output) and weight tensors in bf16
        # In that case we need to cast the input to the weight dtype to avoid dtype mismatch errors.
        # See: https://github.com/pytorch/pytorch/issues/174763
        if hasattr(torch.nn.functional, "grouped_mm"):
            return torch.nn.functional.grouped_mm(input.to(weight.dtype), weight, offs=offs)
        elif hasattr(torch, "_grouped_mm"):
            return torch._grouped_mm(input.to(weight.dtype), weight, offs=offs)

    return torch.ops.transformers.grouped_mm_fallback(input, weight, offs=offs)

