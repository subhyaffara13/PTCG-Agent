
def _varlen_attn_backward(
    grad_out: torch.Tensor,
    query: torch.Tensor,
    key: torch.Tensor,
    value: torch.Tensor,
    out: torch.Tensor,
    lse: torch.Tensor,
    cu_seq_q: torch.Tensor,
    cu_seq_k: torch.Tensor,
    max_q: int,
    max_k: int,
    is_causal: bool,
    rng_state: torch.Tensor,
    scale: float | None = None,
    window_size: list[int] | None = None,
) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
    window_size = _normalize_window_size(window_size)

    unused = torch.empty(0, device=query.device)

    use_cudnn = query.is_cuda and _should_use_cudnn(query.device.index)
    if use_cudnn:
        log.info("Using cuDNN backend for varlen_attn")
        if window_size[0] != -1 or window_size[1] != -1:
            raise RuntimeError(
                "cuDNN backend does not support window attention. Please use Flash Attention backend."
            )
        dq, dk, dv = torch.ops.aten._cudnn_attention_backward(
            grad_out,
            query,
            key,
            value,
            out,
            lse,
            cu_seq_q,
            cu_seq_k,
            max_q,
            max_k,
            0.0,
            is_causal,
            rng_state,
            unused,
            scale=scale,
        )
    else:
        log.info("Using Flash Attention backend for varlen_attn")
        dq, dk, dv = torch.ops.aten._flash_attention_backward(
            grad_out,
            query,
            key,
            value,
            out,
            lse,
            cu_seq_q,
            cu_seq_k,
            max_q,
            max_k,
            0.0,
            is_causal,
            rng_state,
            unused,
            scale=scale,
            window_size_left=window_size[0],
            window_size_right=window_size[1],
        )
    return dq, dk, dv

