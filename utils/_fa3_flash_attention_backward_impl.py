
def _fa3_flash_attention_backward_impl(
    grad_out: torch.Tensor,
    query: torch.Tensor,
    key: torch.Tensor,
    value: torch.Tensor,
    out: torch.Tensor,
    logsumexp: torch.Tensor,
    cum_seq_q: torch.Tensor | None,
    cum_seq_k: torch.Tensor | None,
    max_q: int,
    max_k: int,
    dropout_p: float,
    is_causal: bool,
    rng_state: torch.Tensor,
    unused: torch.Tensor,
    *,
    scale: float | None = None,
    window_size_left: int | None = None,
    window_size_right: int | None = None,
):
    """FA3 implementation of _flash_attention_backward."""
    error = _fa3_backward_support_error(
        grad_out,
        query,
        key,
        value,
        out,
        logsumexp,
        dropout_p,
        cum_seq_q,
        window_size_left,
        window_size_right,
    )

    if error is not None:
        raise RuntimeError(f"FA3 flash_attention backward unsupported: {error}")

    deterministic = torch.are_deterministic_algorithms_enabled()

    dq, dk, dv = _fa3_run_backward(
        grad_out,
        query,
        key,
        value,
        out,
        logsumexp,
        cum_seq_q,
        cum_seq_k,
        max_q,
        max_k,
        scale,
        is_causal,
        window_size_left if window_size_left is not None else -1,
        window_size_right if window_size_right is not None else -1,
        deterministic,
    )
    return dq, dk, dv

