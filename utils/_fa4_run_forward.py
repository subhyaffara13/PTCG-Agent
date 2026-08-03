from typing import Any

def _fa4_run_forward(
    query: torch.Tensor,
    key: torch.Tensor,
    value: torch.Tensor,
    cu_seq_q: torch.Tensor | None,
    cu_seq_k: torch.Tensor | None,
    max_q: int | None,
    max_k: int | None,
    scale: float | None,
    is_causal: bool,
    window_size_left: int | None,
    window_size_right: int | None,
    seqused_k: torch.Tensor | None,
    out: torch.Tensor | None = None,
    block_table: torch.Tensor | None = None,
    num_splits: int | None = None,
) -> tuple[torch.Tensor, torch.Tensor]:
    if _FA4_MODULE_PATH is None:
        raise RuntimeError("FA4 not registered")
    module = _fa4_import_module(_FA4_MODULE_PATH)

    kwargs: dict[str, Any] = {
        "softmax_scale": scale,
        "causal": is_causal,
        "window_size_left": _aten_to_fa4_window_size(window_size_left),
        "window_size_right": _aten_to_fa4_window_size(window_size_right),
        "return_lse": True,
        "cu_seqlens_q": cu_seq_q,
        "cu_seqlens_k": cu_seq_k,
        "max_seqlen_q": max_q,
        "max_seqlen_k": max_k,
        "seqused_k": seqused_k.contiguous() if seqused_k is not None else None,
        "page_table": block_table,
        "num_splits": num_splits or 1,
        "out": out,
    }
    out, lse = module._flash_attn_fwd(query, key, value, **kwargs)
    return out, lse.contiguous()

