
def _fa4_run_backward(
    grad_out: torch.Tensor,
    query: torch.Tensor,
    key: torch.Tensor,
    value: torch.Tensor,
    out: torch.Tensor,
    logsumexp: torch.Tensor,
    cu_seq_q: torch.Tensor | None,
    cu_seq_k: torch.Tensor | None,
    scale: float | None,
    is_causal: bool,
    window_size_left: int | None,
    window_size_right: int | None,
    deterministic: bool = False,
) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
    if _FA4_MODULE_PATH is None:
        raise RuntimeError("FA4 not registered")
    module = _fa4_import_module(_FA4_MODULE_PATH)
    dq, dk, dv = module._flash_attn_bwd(
        query,
        key,
        value,
        out,
        grad_out,
        logsumexp.contiguous(),
        softmax_scale=scale,
        causal=is_causal,
        window_size_left=_aten_to_fa4_window_size(window_size_left),
        window_size_right=_aten_to_fa4_window_size(window_size_right),
        cu_seqlens_q=cu_seq_q,
        cu_seqlens_k=cu_seq_k,
        deterministic=deterministic,
    )
    return dq, dk, dv

