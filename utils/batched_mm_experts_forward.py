
def batched_mm_experts_forward(
    self: torch.nn.Module,
    hidden_states: torch.Tensor,
    top_k_index: torch.Tensor,
    top_k_weights: torch.Tensor,
) -> torch.Tensor:
    num_top_k = top_k_index.size(-1)
    num_tokens = hidden_states.size(0)
    hidden_dim = hidden_states.size(-1)

    # S is the number of selected tokens-experts pairs (S = num_tokens * num_top_k)
    # Replicate each token num_top_k times to align with the flattened (S,) routing tensors.
    selected_hidden_states = hidden_states.repeat_interleave(num_top_k, dim=0)
    sample_weights = top_k_weights.reshape(-1)  # (S,)
    expert_ids = top_k_index.reshape(-1)  # (S,)

    # Clamp EP sentinels so `gate_up_proj[expert_ids]` stays in-bounds. Routing weights are already
    # zero at sentinel slots (RouterParallel masks them at dispatch), so the weighted mul drops
    # those contributions — we pay the wasted GEMM compute because batched_mm has no offset to skip.
    # Out-of-place to avoid mutating the caller's routing tensor (a contiguous `reshape(-1)` aliases it).
    expert_ids = expert_ids.clamp(0, self.num_experts - 1)

    # Select gate_up or just up projection weights and biases
    if self.has_gate:
        selected_weights = self.gate_up_proj[expert_ids]
        selected_biases = self.gate_up_proj_bias[expert_ids] if self.has_bias else None
    else:
        selected_weights = self.up_proj[expert_ids]
        selected_biases = self.up_proj_bias[expert_ids] if self.has_bias else None

    # --- Up projection per expert (batched) ---
    proj_out = _batched_linear(
        selected_hidden_states, selected_weights, bias=selected_biases, is_transposed=self.is_transposed
    )  # (S, 2 * intermediate_dim) or  (S, intermediate_dim) depending on whether we have gating

    # Apply gating or activation
    if self.has_gate:
        # for gated experts we apply the custom/default gating mechanism
        proj_out = self._apply_gate(proj_out)  # (S, intermediate_dim)
    else:
        # for non-gated experts we just apply the activation function
        proj_out = self.act_fn(proj_out)  # (S, intermediate_dim)

    # Select down projection weights and biases for selected samples
    selected_weights = self.down_proj[expert_ids]
    selected_biases = self.down_proj_bias[expert_ids] if self.has_bias else None

    # --- Down projection per expert (batched) ---
    proj_out = _batched_linear(
        proj_out, selected_weights, bias=selected_biases, is_transposed=self.is_transposed
    )  # (S, hidden_dim)

    # Apply routing weights
    weighted_out = proj_out * sample_weights.unsqueeze(-1)  # (S, hidden_dim)

    # Accumulate results using deterministic reshape+sum instead of index_add_
    # index_add_ with duplicate indices is non-deterministic on CUDA due to atomicAdd
    # index_add_ accumulates in-place using the dtype of the output tensor (fp16/bf16)
    # reshape+sum accumulates in fp32 which is more stable for low precision training/inference.
    final_hidden_states = weighted_out.view(num_tokens, num_top_k, hidden_dim).sum(dim=1)

    return final_hidden_states.to(hidden_states.dtype)

