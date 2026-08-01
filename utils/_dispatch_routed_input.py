
def _dispatch_routed_input(
    hidden_states: torch.Tensor,
    top_k_index: torch.Tensor,
    top_k_weights: torch.Tensor,
    num_experts: int,
    m_alignment: int,
    use_psum_layout: bool,
) -> tuple:
    """Sort tokens by expert id and build the M-grouped padded layout.

    Returns `(sorted_hidden_states_g, sample_weights_g, expert_ids_g,
              sentinel_mask, perm, sorted_to_padded, grouped_layout,
              total_padded_rows)`.
    """
    # S is the number of selected token-expert pairs (S = num_tokens * num_top_k)
    num_top_k = top_k_index.size(-1)
    expert_ids = top_k_index.reshape(-1)  # (S,)
    sample_weights = top_k_weights.reshape(-1)  # (S,)

    # Sort by expert for grouped processing
    expert_ids_g, perm = torch.sort(expert_ids)
    sorted_hidden_states_g = hidden_states[perm // num_top_k]
    sample_weights_g = sample_weights[perm]

    # Build the M-grouped padded layout (DeepGEMM contract: each expert's rows
    # start on the kernel's M-alignment boundary, sentinels routed past valid
    # expert blocks).
    sorted_to_padded, grouped_layout, total_padded_rows = _build_deepgemm_contiguous_layout(
        expert_ids_g, num_experts, m_alignment, use_psum_layout
    )

    # EP sentinel mask is captured before the in-place clamp; used by the post-mask in
    # `_combine_routed_output` to zero sentinel rows before the per-token reduction. The clamp
    # keeps any per-row gather (e.g. bias) in-bounds — bias added at sentinel positions falls
    # in rows the kernel skips, so harmless. Safe to mutate now: the layout was built from the
    # unclamped tensor and nothing downstream needs the sentinel info from `expert_ids_g` itself.
    sentinel_mask = (expert_ids_g >= num_experts).unsqueeze(-1)
    expert_ids_g.clamp_(max=num_experts - 1)
    return (
        sorted_hidden_states_g,
        sample_weights_g,
        expert_ids_g,
        sentinel_mask,
        perm,
        sorted_to_padded,
        grouped_layout,
        total_padded_rows,
    )

