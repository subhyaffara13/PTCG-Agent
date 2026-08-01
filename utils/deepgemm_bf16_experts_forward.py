
def deepgemm_bf16_experts_forward(
    self: torch.nn.Module,
    hidden_states: torch.Tensor,
    top_k_index: torch.Tensor,
    top_k_weights: torch.Tensor,
) -> torch.Tensor:
    if hidden_states.dtype != torch.bfloat16:
        raise ValueError(f"DeepGEMM experts path requires bfloat16 hidden states, got {hidden_states.dtype}")

    deepgemm = load_deepgemm_kernel()
    # Non-transposed weights (E, N, K) → NT kernel; transposed (E, K, N) → NN kernel.
    grouped_bf16_matmul = deepgemm.grouped_bf16_matmul_nn if self.is_transposed else deepgemm.grouped_bf16_matmul_nt

    device = hidden_states.device
    num_top_k = top_k_index.size(-1)
    num_tokens = hidden_states.size(0)
    hidden_dim = hidden_states.size(-1)

    (
        sorted_hidden,
        sorted_weights,
        expert_ids_g,
        sentinel_mask,
        perm,
        sorted_to_padded,
        grouped_layout,
        total_padded_rows,
    ) = _dispatch_routed_input(
        hidden_states, top_k_index, top_k_weights, self.num_experts, deepgemm.m_alignment, _is_sm100(device)
    )

    weight_up = to_local(self.gate_up_proj if self.has_gate else self.up_proj)
    weight_down = to_local(self.down_proj)
    up_bias = to_local(self.gate_up_proj_bias if self.has_gate else self.up_proj_bias) if self.has_bias else None
    down_bias = to_local(self.down_proj_bias) if self.has_bias else None

    # Up projection.
    up_out_dim = weight_up.shape[-1] if self.is_transposed else weight_up.shape[1]
    act = _pad_for_deepgemm(sorted_hidden, sorted_to_padded, total_padded_rows)
    proj_out = torch.empty(total_padded_rows, up_out_dim, device=device, dtype=hidden_states.dtype)
    grouped_bf16_matmul(act, weight_up, proj_out, grouped_layout, use_psum_layout=_is_sm100(device))
    if self.has_bias:
        proj_out.index_add_(0, sorted_to_padded, up_bias[expert_ids_g])

    proj_out = self._apply_gate(proj_out) if self.has_gate else self.act_fn(proj_out)

    # Down projection.
    out = torch.empty(total_padded_rows, hidden_dim, device=device, dtype=hidden_states.dtype)
    grouped_bf16_matmul(proj_out, weight_down, out, grouped_layout, use_psum_layout=_is_sm100(device))
    if self.has_bias:
        out.index_add_(0, sorted_to_padded, down_bias[expert_ids_g])

    return _combine_routed_output(
        out,
        sorted_weights,
        sentinel_mask,
        perm,
        sorted_to_padded,
        num_tokens,
        num_top_k,
        hidden_dim,
        hidden_states.dtype,
    )

