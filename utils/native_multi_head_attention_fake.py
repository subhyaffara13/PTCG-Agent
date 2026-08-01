
def native_multi_head_attention_fake(
    query,
    key,
    value,
    embed_dim,
    num_head,
    qkv_weight,
    qkv_bias,
    proj_weight,
    proj_bias,
    mask=None,
    need_weights=True,
    average_attn_weights=True,
    mask_type=None,
):
    if query.is_nested or key.is_nested or value.is_nested:
        raise NotImplementedError(
            "_native_multi_head_attention fake implementation does not support nested tensors"
        )

    if query.numel() == 0:
        return (query.new_empty(query.shape), query.new_empty(0))

    B = query.size(0)  # B: batch size
    T = query.size(1)  # T: target sequence length

    # In native_multi_head_attention_cuda,
    # we have proj = transform0213_gemm_nt_bias(attn_ctx, proj_weight, proj_bias, query)
    # , which does attn_ctx @ proj_weight.T + proj_bias
    # so the last dim of output shape is proj_weight.size(0)
    output_dim = proj_weight.size(0)
    output = query.new_empty(B, T, output_dim)

    if need_weights:
        if average_attn_weights:
            # When averaging attention weights, shape is [B, T, T] (averaged over heads)
            # T = query seq len, S = key/value seq len
            attn_weights = query.new_empty(B, T, T)
        else:
            # When not averaging, shape is [B, num_head, T, T]
            # T = query seq len, S = key/value seq len
            attn_weights = query.new_empty(B, num_head, T, T)
    else:
        attn_weights = query.new_empty(0)

    return (output, attn_weights)

