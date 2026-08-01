
def _fa3_run_backward(
    grad_out: torch.Tensor,
    query: torch.Tensor,
    key: torch.Tensor,
    value: torch.Tensor,
    out: torch.Tensor,
    logsumexp: torch.Tensor,
    cu_seq_q: torch.Tensor | None,
    cu_seq_k: torch.Tensor | None,
    max_seqlen_q: int | None,
    max_seqlen_k: int | None,
    scale: float | None,
    is_causal: bool,
    window_size_left: int,
    window_size_right: int,
    deterministic: bool = False,
) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
    if _FA3_CUDA_BWD is None:
        raise RuntimeError("FA3 not registered")

    # Ensure contiguous
    dout = _maybe_contiguous(grad_out)
    q = query.contiguous() if query.stride(-1) != 1 else query
    k = key.contiguous() if key.stride(-1) != 1 else key
    v = value.contiguous() if value.stride(-1) != 1 else value
    o = _maybe_contiguous(out)
    lse = _maybe_contiguous(logsumexp)

    # Pre-allocate gradient tensors
    dq = torch.empty_like(q)
    dk = torch.empty_like(k)
    dv = torch.empty_like(v)
    _FA3_CUDA_BWD(
        dout,
        q,
        k,
        v,
        o,
        lse,
        dq,
        dk,
        dv,
        cu_seq_q,
        cu_seq_k,
        None,
        None,
        max_seqlen_q,
        max_seqlen_k,
        scale,
        is_causal,
        window_size_left,
        window_size_right,
        0.0,
        deterministic,
        torch._C._get_sm_carveout_experimental() or 0,
    )
    return dq, dk, dv

