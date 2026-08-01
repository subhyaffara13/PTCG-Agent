
def sonicmoe_experts_forward(
    self: torch.nn.Module,
    hidden_states: torch.Tensor,
    top_k_index: torch.Tensor,
    top_k_weights: torch.Tensor,
) -> torch.Tensor:
    if not self.has_gate:
        raise ValueError("sonicmoe requires gated experts (has_gate=True)")
    if hidden_states.device.type != "cuda":
        raise ValueError("sonicmoe requires CUDA device")

    device = hidden_states.device
    num_top_k = top_k_index.size(-1)
    num_tokens = hidden_states.size(0)

    # Flatten — token_indices must be int32, sorted ascending (required by sonic-moe)
    token_idx = torch.arange(num_tokens, device=device).unsqueeze(1).expand(-1, num_top_k).reshape(-1).int()
    router_scores = top_k_weights.reshape(-1).to(hidden_states.dtype)
    expert_ids = top_k_index.reshape(-1).int()

    # EP sentinel handling: leave `expert_ids` unclamped — the kernel's metadata stage drops
    # `expert_ids >= num_experts` from the per-expert histogram and masks them out of the
    # scatter indices, so sentinels never enter the grouped GEMM. Their routing weights are
    # already zero (RouterParallel masks them at dispatch), so the per-token reduction
    # contributes nothing for sentinel slots.

    w1 = to_local(self.gate_up_proj)
    w2 = to_local(self.down_proj)
    b1 = to_local(self.gate_up_proj_bias) if self.has_bias else None
    b2 = to_local(self.down_proj_bias) if self.has_bias else None

    # Map activation function
    act_name = getattr(self.config, "hidden_act", "silu").lower()
    # Permute weights as expected by sonic-moe (E=num_experts, H=hidden_size, I=intermediate_size).
    # Non-transposed: gate_up_proj is (E, 2*I, H), down_proj is (E, H, I) -> permute(1, 2, 0).
    # Transposed: gate_up_proj is (E, H, 2*I), down_proj is (E, I, H) -> permute(2, 1, 0).
    perm = (2, 1, 0) if self.is_transposed else (1, 2, 0)
    w1 = w1.permute(*perm)  # (2*I, H, E)
    w2 = w2.permute(*perm)  # (I, H, E)

    return _sonicmoe_wrapper(
        hidden_states=hidden_states,
        router_scores=router_scores,
        expert_ids=expert_ids,
        token_idx=token_idx,
        w1=w1,
        b1=b1,
        w2=w2,
        b2=b2,
        act_name=act_name,
        num_experts=self.num_experts,
        concat_layout=self.is_concatenated,
        is_inference_mode_enabled=not torch.is_grad_enabled(),
    )

