from typing import Any

def _backward(
    ctx: Any, grad_out: torch.Tensor, grad_lse: torch.Tensor, grad_rng: torch.Tensor
) -> tuple[torch.Tensor | None, ...]:
    query, key, value, cu_seq_q, cu_seq_k, out, lse, rng_state = ctx.saved_tensors

    max_q = ctx.max_q
    max_k = ctx.max_k
    is_causal = ctx.is_causal
    scale = ctx.scale
    window_size = ctx.window_size

    dq, dk, dv = torch.ops.torch_attn._varlen_attn_backward(
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
        is_causal,
        rng_state,
        scale,
        window_size,
    )
    # cu_seq_q, cu_seq_k, max_q, max_k, is_causal, scale, window_size, \
    # enable_gqa, seqused_k, block_table, num_splits
    num_params = 11
    return (dq, dk, dv, *((None,) * num_params))

