
def _fa4_backward_support_error(
    grad_out: torch.Tensor,
    query: torch.Tensor,
    key: torch.Tensor,
    value: torch.Tensor,
    out: torch.Tensor,
    logsumexp: torch.Tensor,
    dropout_p: float,
    cum_seq_q: torch.Tensor | None,
) -> str | None:
    if dropout_p != 0.0:
        return "dropout_p must be 0"
    error = _fa4_common_support_error(
        query,
        (grad_out, query, key, value, out, logsumexp),
        cum_seq_q,
        require_fp32=(("logsumexp", logsumexp),),
    )
    if error is not None:
        return error
    return None

