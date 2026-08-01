
def deepgemm_fp8_fp4_megamoe_experts_forward(
    self: torch.nn.Module,
    hidden_states: torch.Tensor,
    top_k_index: torch.Tensor,
    top_k_weights: torch.Tensor,
    process_group: torch.distributed.ProcessGroup | None = None,
) -> torch.Tensor:
    """FP8 acts × FP4 weights Mega MoE forward (SM100+).

    Fuses EP dispatch + L1 + SwiGLU + L2 + EP combine into one kernel,
    overlapping NVLink with tensor-core compute. The kernel handles the full
    `(num_tokens, hidden) → (num_tokens, hidden)` MoE forward including the
    weighted top-k reduction; the caller must NOT all-reduce the output.

    `process_group` is supplied automatically by `MoeTensorParalellExperts._prepare_input_fn`
    when the module is wrapped for TP — it's required for the symm-buffer rendezvous
    on first forward. `top_k_index` is GLOBAL expert ids (`-1` marks skipped slots).

    Caller-managed `self` attributes:
      - `gate_up_proj`, `gate_up_proj_scale_inv`: L1 weight + UE8M0 SF.
      - `down_proj`, `down_proj_scale_inv`: L2 weight + UE8M0 SF.
      Both pairs must be transformed together via
      `transform_weights_for_mega_moe((gate_up, gate_up_sf), (down, down_sf))`.
      - `config.swiglu_limit` (optional): SwiGLU clamp; absent → unclamped.
    """
    if self.gate_up_proj.dtype != torch.int8:
        raise RuntimeError(
            f"DeepGEMM Mega MoE requires FP4-packed expert weights (dtype=`int8`), got "
            f"`{self.gate_up_proj.dtype}`. Use the 'deepgemm' dispatch for FP8 experts."
        )

    if process_group is None:
        raise ValueError(
            "DeepGEMM Mega MoE requires a `process_group` for the EP group. The TP wrapping "
            "(MoeTensorParalellMegaMoeExperts) supplies it automatically; pass it explicitly otherwise."
        )

    deepgemm = load_deepgemm_kernel(requires_sm100=True)

    # First-forward one-shot: pack UE8M0 SFs and interleave the L1/L2 weights for UTCCP.
    # Kept lazy here (instead of in a quantizer load-time hook) so the megamoe-specific
    # setup lives alongside the megamoe forward — `set_experts_implementation` refuses
    # to flip in/out of `deepgemm_megamoe` at runtime, so the flag won't go stale.
    if not getattr(self, "_megamoe_transformed", False):
        setup_megamoe_weights(self)
        self._megamoe_transformed = True

    num_top_k = top_k_index.size(-1)
    num_tokens = hidden_states.size(0)
    hidden_dim = hidden_states.size(-1)
    num_local_experts = self.gate_up_proj.size(0)
    intermediate_hidden = self.gate_up_proj.size(1) // 2
    num_global_experts = num_local_experts * process_group.size()

    # Lazily (re)allocate the symmetric buffer when the cached one is too small.
    if getattr(self, "symm_buffer", None) is None or self.symm_buffer.num_max_tokens_per_rank < num_tokens:
        self.symm_buffer = deepgemm.get_symm_buffer_for_mega_moe(
            process_group,
            hidden=hidden_dim,
            num_topk=num_top_k,
            num_experts=num_global_experts,
            num_max_tokens_per_rank=num_tokens,
            intermediate_hidden=intermediate_hidden,
        )

    x_fp8, x_sf = deepgemm.per_token_cast_to_fp8(hidden_states, use_ue8m0=True, gran_k=32, use_packed_ue8m0=True)
    self.symm_buffer.x[:num_tokens].copy_(x_fp8)
    self.symm_buffer.x_sf[:num_tokens].copy_(x_sf)
    self.symm_buffer.topk_idx[:num_tokens].copy_(top_k_index)
    self.symm_buffer.topk_weights[:num_tokens].copy_(top_k_weights)

    # `activation_clamp` must match `_apply_gate`'s clamp on the regular path so the kernel's
    # fused SwiGLU sees the same value range the model was calibrated for.
    y = torch.empty((num_tokens, hidden_dim), dtype=torch.bfloat16, device=hidden_states.device)
    deepgemm.fp8_fp4_mega_moe(
        y,
        (self.gate_up_proj, self.gate_up_proj_scale_inv),
        (self.down_proj, self.down_proj_scale_inv),
        self.symm_buffer,
        activation_clamp=getattr(getattr(self, "config", None), "swiglu_limit", None),
    )
    return y.to(hidden_states.dtype)

