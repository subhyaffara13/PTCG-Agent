
def _varlen_attn_out_fake(
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
    Fake implementation for meta tensor computation and tracing.
    """
    total_q = query.size(0)
    num_heads = query.size(1)
    logsumexp = torch.empty(
        (num_heads, total_q), dtype=torch.float, device=query.device
    )

    if torch.version.hip:
        preferred = torch._C._get_rocm_fa_preferred_backend()
        if preferred == torch._C._ROCmFABackend.AOTriton:
            batch_size = cu_seq_q.size(0) - 1
            logsumexp = torch.empty(
                (batch_size, num_heads, max_q), dtype=torch.float, device=query.device
            )

    return logsumexp

