
def fp8_batched_mm_experts_forward(
    self: torch.nn.Module,
    hidden_states: torch.Tensor,
    top_k_index: torch.Tensor,
    top_k_weights: torch.Tensor,
) -> torch.Tensor:
    if self.activation_scheme == "static":
        raise NotImplementedError(
            "batched_mm experts dispatch does not support activation_scheme='static'. "
            "Use the default eager dispatch or switch to activation_scheme='dynamic'."
        )

    finegrained_fp8 = load_finegrained_fp8_kernel()

    num_top_k = top_k_index.size(-1)
    num_tokens = hidden_states.size(0)
    hidden_dim = hidden_states.size(-1)

    # S is the number of selected tokens-experts pairs (S = num_tokens * num_top_k)
    # Replicate each token num_top_k times to align with the flattened (S,) routing tensors.
    selected_hidden_states = hidden_states.repeat_interleave(num_top_k, dim=0)
    sample_weights = top_k_weights.reshape(-1)  # (S,)
    expert_ids = top_k_index.reshape(-1)  # (S,)

    # EP sentinel handling: leave `expert_ids` unclamped — the batched kernel early-returns on
    # `expert_id >= NUM_EXPERTS`, leaving sentinel output rows uninitialized. The post-mask below
    # zeroes them before the per-token reduction so `uninit * 0 = NaN` can't poison the sum.
    sentinel_mask = (expert_ids >= self.num_experts).unsqueeze(-1)

    weight_up = to_local(self.gate_up_proj if self.has_gate else self.up_proj)
    weight_scale_up = to_local(self.gate_up_proj_scale_inv if self.has_gate else self.up_proj_scale_inv)
    weight_down = to_local(self.down_proj)
    weight_scale_down = to_local(self.down_proj_scale_inv)

    # --- Up projection per expert (FP8 batched) ---
    proj_out = finegrained_fp8.batched_matmul(
        selected_hidden_states,
        weight_up,
        weight_scale_up,
        block_size=self.block_size,
        expert_ids=expert_ids,
    )  # (S, 2 * intermediate_dim) or (S, intermediate_dim) depending on gating

    # Apply gating or activation
    if self.has_gate:
        # for gated experts we apply the custom/default gating mechanism
        proj_out = self._apply_gate(proj_out)  # (S, intermediate_dim)
    else:
        # for non-gated experts we just apply the activation function
        proj_out = self.act_fn(proj_out)  # (S, intermediate_dim)

    # --- Down projection per expert (FP8 batched) ---
    proj_out = finegrained_fp8.batched_matmul(
        proj_out,
        weight_down,
        weight_scale_down,
        block_size=self.block_size,
        expert_ids=expert_ids,
    )  # (S, hidden_dim)

    # Apply routing weights
    weighted_out = proj_out * sample_weights.to(proj_out.dtype).unsqueeze(-1)  # (S, hidden_dim)

    # Post-mask sentinel rows: kernel left them uninitialized, so zero them out
    # before the reduction below (uninit may be NaN; NaN * 0 = NaN).
    weighted_out.masked_fill_(sentinel_mask, 0.0)

    # Accumulate results using deterministic reshape+sum instead of index_add_
    # (index_add_ with duplicate indices is non-deterministic on CUDA due to atomicAdd)
    final_hidden_states = weighted_out.view(num_tokens, num_top_k, hidden_dim).sum(dim=1)

    return final_hidden_states.to(hidden_states.dtype)

