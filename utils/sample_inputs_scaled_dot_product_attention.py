
def sample_inputs_scaled_dot_product_attention(op_info, device, dtype, requires_grad, **kwargs):
    make = partial(make_tensor, device=device, dtype=dtype, requires_grad=requires_grad)
    batch, seq_q, seq_kv, num_heads, head_dim = 4, 3, 6, 4, 8

    dim_3_q_shape = (batch, seq_q, head_dim)
    dim_3_kv_shape = (batch, seq_kv, head_dim)
    dim_4_q_shape = (batch, num_heads, seq_q, head_dim)
    dim_4_kv_shape = (batch, num_heads, seq_kv, head_dim)

    broadcast_tuple = ((num_heads, seq_q, head_dim), (batch, num_heads, seq_kv, head_dim))

    qkv_shapes = [(dim_3_q_shape, dim_3_kv_shape), (dim_4_q_shape, dim_4_kv_shape), broadcast_tuple]
    samples = []
    gqa_options = [True, False]
    causal_options = [True, False]
    for qkv_shape, is_causal, dropout_p, _enable_gqa in product(
            qkv_shapes, causal_options, [0.0, 0.5], gqa_options):
        shape_q, shape_kv = qkv_shape
        samples.append(SampleInput(
            make(shape_q),
            make(shape_kv),
            make(shape_kv),
            is_causal=is_causal,
            dropout_p=dropout_p
        ))

    # Add non standard shapes
    # FIXME(rec): should diff_v_head_dim be appended to samples?
    diff_v_head_dim = SampleInput(  # noqa: F841
        make((batch, num_heads, seq_q, head_dim)),
        make((batch, num_heads, seq_kv, head_dim)),
        make((batch, num_heads, seq_kv, head_dim + 8)),
        is_causal=is_causal,
        dropout_p=dropout_p
    )

    # Add an attn_mask
    samples.append(
        SampleInput(
            make((batch, num_heads, seq_q, head_dim)),
            make((batch, num_heads, seq_kv, head_dim)),
            make((batch, num_heads, seq_kv, head_dim)),
            attn_mask=make((seq_q, seq_kv)),
            is_causal=False,
            dropout_p=0.0)
    )

    yield from samples

