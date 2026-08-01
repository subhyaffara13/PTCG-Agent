
def flex_attention_grid(batch_size, q_heads, num_queries, d_model, meta, *, cdiv):
    """How is this kernel parallelized?
    We create a grid of (ceil_div(n_queries, query_block_size), batch_size, num_heads)
    Each block is responsible for iterating over blocks of keys and values calculating
    the final attention output.
    """
    return (cdiv(num_queries, meta["BLOCK_M"]), batch_size, q_heads)

