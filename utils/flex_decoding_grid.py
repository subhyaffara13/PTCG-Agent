
def flex_decoding_grid(batch_size, kv_heads, gqa_group_size, seq_len_q, d_model, meta):
    """How is this kernel parallelized?
    We create a grid of (batch_size * kv_heads, SPLIT_KV, 1)
    Each block is responsible for iterating over blocks of keys and values calculating
    the local output for their tile of keys and values over all full length of query.
    groups of SPLIT_KV blocks then combine their output to produce the final result.
    """

    BLOCK_M = meta["BLOCK_M"]
    num_block_m = ceildiv(seq_len_q * gqa_group_size, BLOCK_M)
    return (num_block_m, batch_size * kv_heads, meta["SPLIT_KV"])

