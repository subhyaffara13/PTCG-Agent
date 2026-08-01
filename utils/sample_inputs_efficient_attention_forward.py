
def sample_inputs_efficient_attention_forward(op_info, device, dtype, requires_grad, **kwargs):
    make = partial(make_tensor, device=device, dtype=dtype, requires_grad=requires_grad)
    batch, num_heads, head_dim = 4, 4, 8
    seq_q = 11
    seq_kv = 32

    dim_4_q_shape = (batch, num_heads, seq_q, head_dim)
    dim_4_kv_shape = (batch, num_heads, seq_kv, head_dim)

    qkv_shapes = [(dim_4_q_shape, dim_4_kv_shape)]
    samples = []
    mask_types = [1, 2]  # UpperLeft, LowerRight
    scales = [None, 1.0]

    for qkv_shape, _is_causal, dropout_p, mask_type, scale in product(
            qkv_shapes, [True, False], [0.0, 0.5], mask_types, scales):
        shape_q, shape_kv = qkv_shape
        samples.append(SampleInput(
            make(shape_q).transpose(1, 2),
            make(shape_kv).transpose(1, 2),
            make(shape_kv).transpose(1, 2),
            bias=None,
            cu_seqlens_q=None,
            cu_seqlens_k=None,
            max_seqlen_q=None,
            max_seqlen_k=None,
            dropout_p=dropout_p,
            custom_mask_type=mask_type,
            compute_log_sumexp=requires_grad,
            scale=scale,
            seqlen_k=None
        ))

    # Add non standard shapes
    # FIXME(rec): should diff_v_head_dim be appended to samples?
    diff_v_head_dim = SampleInput(  # noqa: F841
        make((batch, seq_q, num_heads, head_dim)),
        make((batch, seq_kv, num_heads, head_dim)),
        make((batch, seq_kv, num_heads, head_dim + 8)),
        bias=None,
        cu_seqlens_q=None,
        cu_seqlens_k=None,
        max_seqlen_q=None,
        max_seqlen_k=None,
        dropout_p=dropout_p,
        custom_mask_type=0,  # No Mask
        compute_log_sumexp=requires_grad,
        scale=None,
        seqlen_k=None
    )

    # Add an attn_mask
    samples.append(
        SampleInput(
            make((batch, seq_q, num_heads, head_dim)),
            make((batch, seq_kv, num_heads, head_dim)),
            make((batch, seq_kv, num_heads, head_dim)),
            bias=make(batch, num_heads, seq_q, seq_kv),
            cu_seqlens_q=None,
            cu_seqlens_k=None,
            max_seqlen_q=None,
            max_seqlen_k=None,
            dropout_p=dropout_p,
            custom_mask_type=0,  # No Mask
            compute_log_sumexp=requires_grad,
            scale=None,
            seqlen_k=None
        )
    )

    # jagged (with query/keys offsets)
    cu_seqlens_k = torch.arange(-1, 32 * 2 + 1, 2, dtype=torch.int32, device=device)
    cu_seqlens_k[-1] = 62
    cu_seqlens_k[0] = 0
    samples.append(
        SampleInput(
            make((32, 2, 64)).view(-1, 8, 8).unsqueeze(0),
            make((64, 64)).view(-1, 8, 8).unsqueeze(0),
            make((64, 64)).view(-1, 8, 8).unsqueeze(0),
            bias=None,
            cu_seqlens_q=torch.arange(0, 32 * 2 + 2, 2, dtype=torch.int32, device=device),
            cu_seqlens_k=cu_seqlens_k,
            max_seqlen_q=2,
            max_seqlen_k=2,
            dropout_p=0.0,
            custom_mask_type=0,  # No Mask
            compute_log_sumexp=requires_grad,
            scale=None,
            seqlen_k=None,
        )
    )

    yield from samples

