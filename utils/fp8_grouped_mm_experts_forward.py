
def fp8_grouped_mm_experts_forward(
    self: torch.nn.Module,
    hidden_states: torch.Tensor,
    top_k_index: torch.Tensor,
    top_k_weights: torch.Tensor,
) -> torch.Tensor:
    if self.activation_scheme == "static":
        raise NotImplementedError(
            "grouped_mm experts dispatch does not support activation_scheme='static'. "
            "Use the default eager dispatch or switch to activation_scheme='dynamic'."
        )

    finegrained_fp8 = load_finegrained_fp8_kernel()

    device = hidden_states.device
    num_top_k = top_k_index.size(-1)
    num_tokens = hidden_states.size(0)
    hidden_dim = hidden_states.size(-1)

    # S is the number of selected token-expert pairs (S = num_tokens * num_top_k)
    sample_weights = top_k_weights.reshape(-1)  # (S,)
    expert_ids = top_k_index.reshape(-1)  # (S,)

    # Sort by expert for grouped processing
    expert_ids_g, perm = torch.sort(expert_ids)
    selected_hidden_states_g = hidden_states[perm // num_top_k]
    sample_weights_g = sample_weights[perm]

    # Compute offsets for grouped processing.
    # histc instead of bincount avoids cuda-graph issues;
    # CPU requires float input, CUDA requires int input (deterministic mode).
    histc_input = expert_ids_g.float() if device.type == "cpu" else expert_ids_g.int()
    tokens_per_expert = torch.histc(histc_input, bins=self.num_experts, min=0, max=self.num_experts - 1)
    offsets = torch.cumsum(tokens_per_expert, dim=0, dtype=torch.int32)

    # EP sentinel handling: leave `expert_ids` unclamped so the sort pushes sentinels to the tail,
    # `histc(max=num_experts-1)` drops them from `tokens_per_expert`, and the grouped matmul skips
    # rows beyond `offsets[-1]` — sentinels cost no real GEMM compute. The kernel writes only
    # valid rows, so sentinel-tail `proj_out` rows are uninit; without the post-mask below,
    # `proj_out[sentinel] * 0 = NaN * 0 = NaN` would poison the per-token reduction. FP8
    # quantized weights are inference-only, so no bwd pre-mask is needed.
    sentinel_mask = (expert_ids_g >= self.num_experts).unsqueeze(-1)

    weight_up = to_local(self.gate_up_proj if self.has_gate else self.up_proj)
    weight_scale_up = to_local(self.gate_up_proj_scale_inv if self.has_gate else self.up_proj_scale_inv)
    weight_down = to_local(self.down_proj)
    weight_scale_down = to_local(self.down_proj_scale_inv)

    # --- Up projection per expert (FP8 grouped) ---
    proj_out = finegrained_fp8.grouped_matmul(
        selected_hidden_states_g,
        weight_up,
        weight_scale_up,
        offsets=offsets,
        tokens_per_expert=tokens_per_expert,
        block_size=self.block_size,
    )  # (S, 2 * intermediate_dim)

    # Apply gating or activation
    if self.has_gate:
        # for gated experts we apply the custom/default gating mechanism
        proj_out = self._apply_gate(proj_out)  # (S, intermediate_dim)
    else:
        # for non-gated experts we just apply the activation function
        proj_out = self.act_fn(proj_out)  # (S, intermediate_dim)

    # --- Down projection per expert (FP8 grouped) ---
    proj_out = finegrained_fp8.grouped_matmul(
        proj_out,
        weight_down,
        weight_scale_down,
        offsets=offsets,
        tokens_per_expert=tokens_per_expert,
        block_size=self.block_size,
    )  # (S, hidden_dim)

    # Apply routing weights
    weighted_out = proj_out * sample_weights_g.to(proj_out.dtype).unsqueeze(-1)  # (S, hidden_dim)

    # Post-mask (fwd path).
    weighted_out.masked_fill_(sentinel_mask, 0.0)

    # Restore original order
    inv_perm = torch.empty_like(perm)
    inv_perm[perm] = torch.arange(perm.size(0), device=device)
    weighted_out = weighted_out[inv_perm]

    # Accumulate results using deterministic reshape+sum instead of index_add_
    # (index_add_ with duplicate indices is non-deterministic on CUDA due to atomicAdd)
    final_hidden_states = weighted_out.view(num_tokens, num_top_k, hidden_dim).sum(dim=1)

    return final_hidden_states.to(hidden_states.dtype)

