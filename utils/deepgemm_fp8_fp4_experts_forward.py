
def deepgemm_fp8_fp4_experts_forward(
    self: torch.nn.Module,
    hidden_states: torch.Tensor,
    top_k_index: torch.Tensor,
    top_k_weights: torch.Tensor,
) -> torch.Tensor:
    _assert_single_device(hidden_states.device, context="experts")

    if self.activation_scheme == "static":
        raise NotImplementedError("DeepGEMM experts dispatch does not support static activation quantization.")
    if hidden_states.dtype != torch.bfloat16:
        raise ValueError(f"DeepGEMM experts path requires bfloat16 hidden states, got {hidden_states.dtype}")

    deepgemm = load_deepgemm_kernel(requires_sm100=self.down_proj.dtype == torch.int8)
    grouped_fp8_fp4_matmul = (
        deepgemm.grouped_fp8_fp4_matmul_nn if self.is_transposed else deepgemm.grouped_fp8_fp4_matmul_nt
    )

    device = hidden_states.device
    num_top_k = top_k_index.size(-1)
    num_tokens = hidden_states.size(0)
    hidden_dim = hidden_states.size(-1)

    weight_up = to_local(self.gate_up_proj if self.has_gate else self.up_proj)
    weight_scale_up = to_local(self.gate_up_proj_scale_inv if self.has_gate else self.up_proj_scale_inv)
    weight_down = to_local(self.down_proj)
    weight_scale_down = to_local(self.down_proj_scale_inv)

    cast_kwargs = _select_fp8_cast_kwargs(weight_up, weight_scale_up, self.block_size, _is_sm100(device))
    (
        sorted_hidden,
        sorted_weights,
        _expert_ids_g,
        sentinel_mask,
        perm,
        sorted_to_padded,
        grouped_layout,
        total_padded_rows,
    ) = _dispatch_routed_input(
        hidden_states, top_k_index, top_k_weights, self.num_experts, deepgemm.m_alignment, _is_sm100(device)
    )
    sf_recipe = (1, 1, cast_kwargs["gran_k"]) if cast_kwargs.get("use_packed_ue8m0") else None

    # Up projection.
    act_fp8, act_scales = deepgemm.per_token_cast_to_fp8(sorted_hidden, **cast_kwargs)
    act_fp8 = _pad_for_deepgemm(act_fp8, sorted_to_padded, total_padded_rows)
    act_scales = _pad_for_deepgemm(act_scales, sorted_to_padded, total_padded_rows)
    proj_out = torch.empty(total_padded_rows, weight_up.shape[1], device=device, dtype=torch.bfloat16)
    grouped_fp8_fp4_matmul(
        (act_fp8, _coerce_sf_for_kernel(act_scales, expected_mn=total_padded_rows)),
        (weight_up, _coerce_sf_for_kernel(weight_scale_up, expected_mn=weight_up.size(-2))),
        proj_out,
        grouped_layout,
        recipe=sf_recipe,
        use_psum_layout=_is_sm100(device),
    )
    proj_out = self._apply_gate(proj_out) if self.has_gate else self.act_fn(proj_out)

    # Down projection.
    proj_fp8, proj_scales = deepgemm.per_token_cast_to_fp8(proj_out, **cast_kwargs)
    out = torch.empty(total_padded_rows, hidden_dim, device=device, dtype=torch.bfloat16)
    grouped_fp8_fp4_matmul(
        (proj_fp8, _coerce_sf_for_kernel(proj_scales, expected_mn=total_padded_rows)),
        (weight_down, _coerce_sf_for_kernel(weight_scale_down, expected_mn=weight_down.size(-2))),
        out,
        grouped_layout,
        recipe=sf_recipe,
        use_psum_layout=_is_sm100(device),
    )

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

