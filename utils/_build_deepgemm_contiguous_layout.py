
def _build_deepgemm_contiguous_layout(
    expert_ids_sorted: torch.Tensor, num_experts: int, alignment: int, use_psum_layout: bool
) -> tuple[torch.Tensor, torch.Tensor, int]:
    """Build the TMA-aligned grouped layout DeepGEMM expects.

    Returns `(sorted_to_padded, grouped_layout, total_padded_rows)`:
      - `grouped_layout` is per-row expert id (Hopper, with `-1` for padding /
        sentinels) or a cumsum of aligned per-expert counts (Blackwell).
      - EP sentinels (values == `num_experts`) are routed past the last expert
        block so DeepGEMM skips them.
    """
    device = expert_ids_sorted.device
    num_tokens = expert_ids_sorted.size(0)
    # `histc` drops values > max, so EP sentinels (== num_experts) don't count.
    tokens_per_expert = torch.histc(expert_ids_sorted.int(), bins=num_experts, min=0, max=num_experts - 1).long()
    aligned_tokens_per_expert = ((tokens_per_expert + alignment - 1) // alignment) * alignment
    # Upper bound — avoids GPU→CPU sync; padding rows are skipped.
    total_padded_rows = num_tokens + min(num_tokens, num_experts) * (alignment - 1)

    # Exclusive cumsum of per-expert padding (index `num_experts` = total padding,
    # which routes EP sentinels past all aligned blocks on Blackwell).
    padding_per_expert = aligned_tokens_per_expert - tokens_per_expert
    cumulative_padding = torch.nn.functional.pad(padding_per_expert.cumsum(0), (1, 0))
    sorted_to_padded = torch.arange(num_tokens, device=device) + cumulative_padding[expert_ids_sorted]

    if use_psum_layout:  # SM100+: kernel reads cumsum of aligned counts as expert boundaries.
        grouped_layout = aligned_tokens_per_expert.cumsum(0).int()
    else:  # SM90: per-row expert id, -1 = skip (padding & sentinels).
        grouped_layout = torch.full((total_padded_rows,), -1, device=device, dtype=torch.int32)
        grouped_layout[sorted_to_padded] = torch.where(expert_ids_sorted < num_experts, expert_ids_sorted.int(), -1)

    return sorted_to_padded, grouped_layout, total_padded_rows

