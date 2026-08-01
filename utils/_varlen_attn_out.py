
def _varlen_attn_out(
    out: torch.Tensor,
    query: torch.Tensor,
    key: torch.Tensor,
    value: torch.Tensor,
    cu_seq_q: torch.Tensor,
    cu_seq_k: torch.Tensor | None,
    max_q: int,
    max_k: int,
    is_causal: bool = False,
    scale: float | None = None,
    window_size: list[int] | None = None,
    enable_gqa: bool = False,
    seqused_k: torch.Tensor | None = None,
    block_table: torch.Tensor | None = None,
    num_splits: int | None = None,
) -> torch.Tensor:
    """
    Private custom op for variable-length attention with pre-allocated output.
    Same as _varlen_attn but writes the attention output into the provided out tensor.
    """
    window_size = _normalize_window_size(window_size)

    use_cudnn = query.is_cuda and _should_use_cudnn(query.device.index)

    if use_cudnn:
        # TODO: look into this
        raise RuntimeError("cuDNN backend does not support out variant.")

    log.info("Using Flash Attention backend for varlen_attn_out")
    softmax_lse = torch.ops.aten._flash_attention_forward_no_dropout_inplace(
        out,
        query,
        key,
        value,
        cu_seq_q,
        cu_seq_k,
        max_q,
        max_k,
        0.0,  # dropout_p hardcoded to 0.0
        is_causal,
        False,  # return_debug_mask
        scale=scale,
        window_size_left=window_size[0],
        window_size_right=window_size[1],
        seqused_k=seqused_k,
        block_table=block_table,
        num_splits=num_splits,
    )

    return softmax_lse

