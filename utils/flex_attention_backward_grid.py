
def flex_attention_backward_grid(
    batch_size, q_heads, num_queries, d_model, kv_heads, num_key_value, meta, *, cdiv
):
    """How is this kernel parallelized?
    We create a grid of (ceil_div(n_queries, query_block_size) * heads_ratio + ceil_div(n_kv, kv_block_size), batch_size, kv_heads)
    Currently this is only parallelizing over batch* kv_heads, but we can, and want to
    parallelize over ceil_div(q_heads//kv_heads * num_key_value, key_value_block_size).
    To do this will either require atomic updates to some grad values or to have a two pass kernel design.
    """
    return (
        cdiv(num_queries, meta["BLOCK_M2"]) * (q_heads // kv_heads)
        + cdiv(num_key_value, meta["BLOCK_N1"]),
        batch_size,
        kv_heads,
    )

