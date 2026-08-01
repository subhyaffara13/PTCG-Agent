
def _grouped_mm_fallback(input: torch.Tensor, weight: torch.Tensor, offs: torch.Tensor) -> torch.Tensor:
    """
    Fallback grouped matrix multiplication used when `torch.nn.functional.grouped_mm` and `torch._grouped_mm`
    are unavailable or incompatible with `torch.compile` (e.g. non-bfloat16 weights).

    Args:
        input (`torch.Tensor`): Input of shape (S, input_dim), sorted by expert id.
        weight (`torch.Tensor`): Expert weights of shape (num_experts, input_dim, output_dim).
        offs (`torch.Tensor`): Cumulative token counts per expert of shape (num_experts,).
    Returns:
        `torch.Tensor`: Output of shape (S, output_dim).
    """
    output = torch.zeros(input.size(0), weight.size(2), device=input.device, dtype=input.dtype)  # (S, output_dim)

    start = 0
    # single cpu<->gpu sync point here,
    # avoids multiple syncs inside the loop
    for i, end in enumerate(offs.tolist()):
        if start == end:
            continue
        torch.mm(input[start:end], weight[i], out=output[start:end])
        start = end

    return output

