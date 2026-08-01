
def _setup_context(ctx: Any, inputs: tuple[Any, ...], output: Any) -> None:
    (
        query,
        key,
        value,
        cu_seq_q,
        cu_seq_k,
        max_q,
        max_k,
        is_causal,
        scale,
        window_size,
        enable_gqa,
        seqused_k,
        block_table,
        num_splits,
    ) = inputs
    out, lse, rng_state = output

    if seqused_k is not None:
        raise RuntimeError("seqused_k is an inference-only parameter.")
    if block_table is not None:
        raise RuntimeError("block_table is an inference-only parameter.")

    ctx.save_for_backward(query, key, value, cu_seq_q, cu_seq_k, out, lse, rng_state)

    ctx.max_q = max_q
    ctx.max_k = max_k
    ctx.is_causal = is_causal
    ctx.scale = scale
    ctx.window_size = window_size

