
def grouped_mm_experts_forward(
    self: torch.nn.Module,
    hidden_states: torch.Tensor,
    top_k_index: torch.Tensor,
    top_k_weights: torch.Tensor,
) -> torch.Tensor:
    device = hidden_states.device
    num_top_k = top_k_index.size(-1)
    num_tokens = hidden_states.size(0)
    hidden_dim = hidden_states.size(-1)

    # S is the number of selected tokens-experts pairs (S = num_tokens * num_top_k)
    sample_weights = top_k_weights.reshape(-1)  # (S,)
    expert_ids = top_k_index.reshape(-1)  # (S,)

    # Sort by expert for grouped processing
    expert_ids_g, perm = torch.sort(expert_ids)
    selected_hidden_states_g = hidden_states[perm // num_top_k]
    sample_weights_g = sample_weights[perm]

    # Compute offsets for grouped_mm
    # using histc instead of bincount to avoid cuda graph issues
    # With deterministic algorithms, CPU only supports float input, CUDA only supports int input.
    # torch.histc() does not support integer dtypes on CPU and MPS.
    histc_input = expert_ids_g.float() if device.type in ("cpu", "mps") else expert_ids_g.int()
    tokens_per_expert = torch.histc(histc_input, bins=self.num_experts, min=0, max=self.num_experts - 1)
    offsets = torch.cumsum(tokens_per_expert, dim=0, dtype=torch.int32)

    # EP sentinel handling: leave `expert_ids` unclamped so the sort pushes sentinels to the tail,
    # `histc(max=num_experts-1)` drops them from `tokens_per_expert`, and grouped_mm skips rows
    # beyond `offsets[-1]` — sentinels cost no real GEMM compute. The kernel leaves sentinel-tail
    # rows of its output uninit (both fwd output and bwd `d_input`), but ONE pre-mask + ONE
    # post-mask covers the whole forward — no per-grouped_mm masking is needed, because
    # intermediate sentinel-row NaN is only ever consumed by the next grouped_mm, which itself
    # only reads rows `< offsets[-1]`:
    #   - fwd post-mask on `weighted_out`: kills `proj_out[sentinel] * 0 = NaN * 0 = NaN`
    #     before the per-token reduction sums it.
    #   - bwd pre-mask on `selected_hidden_states_g`: its `masked_fill_` backward zeros sentinel
    #     rows of `d_selected_hidden_states_g` after the up grouped_mm bwd writes them as
    #     uninit, and before the gather's scatter-add pushes them into `d_hidden_states`.
    # In-place clamp on `expert_ids_g` keeps the per-row bias gather in-bounds (bias added at
    # sentinel positions falls in rows the kernel skips, so harmless). Safe to mutate now —
    # nothing downstream needs the sentinel info from `expert_ids_g` itself.
    sentinel_mask = (expert_ids_g >= self.num_experts).unsqueeze(-1)
    expert_ids_g.clamp_(max=self.num_experts - 1)

    # Select expert weights and biases
    # NOTE: We keep all experts here and rely on offsets to target the active ones.
    # I have already implemented a version that only passes the active experts, but
    # to do so I had to use torch.unique which breaks the graph capture (data-dependent).
    # Also there were no speedup gains from it in my experiments, even in eager mode.
    # NOTE: The grouped_mm kernel only targets the active experts / tokens via the offsets
    if self.has_gate:
        selected_weights = self.gate_up_proj
        selected_biases = self.gate_up_proj_bias[expert_ids_g] if self.has_bias else None
    else:
        selected_weights = self.up_proj
        selected_biases = self.up_proj_bias[expert_ids_g] if self.has_bias else None

    # Pre-mask (bwd path).
    selected_hidden_states_g.masked_fill_(sentinel_mask, 0.0)

    # --- Up projection per expert (grouped) ---
    proj_out = _grouped_linear(
        selected_hidden_states_g, selected_weights, offsets, bias=selected_biases, is_transposed=self.is_transposed
    )  # (S, 2 * intermediate_dim) or  (S, intermediate_dim) depending on whether we have gating

    # Apply gating or activation
    if self.has_gate:
        # for gated experts we apply the custom/default gating mechanism
        proj_out = self._apply_gate(proj_out)  # (S, intermediate_dim)
    else:
        # for non-gated experts we just apply the activation function
        proj_out = self.act_fn(proj_out)  # (S, intermediate_dim)

    # Select down projection weights and biases
    selected_weights = self.down_proj
    selected_biases = self.down_proj_bias[expert_ids_g] if self.has_bias else None

    # --- Down projection per expert (grouped) ---
    proj_out = _grouped_linear(
        proj_out, selected_weights, offsets, bias=selected_biases, is_transposed=self.is_transposed
    )  # (S, hidden_dim)

    # Apply routing weights
    weighted_out = proj_out * sample_weights_g.unsqueeze(-1)  # (S, hidden_dim)

    # Post-mask (fwd path).
    weighted_out.masked_fill_(sentinel_mask, 0.0)

    # Restore original order
    inv_perm = torch.empty_like(perm)
    inv_perm[perm] = torch.arange(perm.size(0), device=device)
    weighted_out = weighted_out[inv_perm]  # (S, hidden_dim)

    # Accumulate results using deterministic reshape+sum instead of index_add_
    # index_add_ with duplicate indices is non-deterministic on CUDA due to atomicAdd
    # index_add_ accumulates in-place using the dtype of the output tensor (fp16/bf16)
    # reshape+sum accumulates in fp32 which is more stable for low precision training/inference.
    final_hidden_states = weighted_out.view(num_tokens, num_top_k, hidden_dim).sum(dim=1)

    return final_hidden_states.to(hidden_states.dtype)

