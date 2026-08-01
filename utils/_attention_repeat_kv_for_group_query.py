
def _attention_repeat_kv_for_group_query(
    query: TFloat, key: TFloat, value: TFloat, op: Opset
) -> tuple[TFloat, TFloat]:
    """Expand key and value for group query attention.

    repeat_interleave is applied on key and value to match the number of heads in query.

    Args:
        query: Tensor of shape [B, q_num_heads, q_S, E]
        key: Tensor of shape [B, k_num_heads, kv_S, E]
        value: Tensor of shape [B, v_num_heads, kv_S, E]

    Returns:
        Tuple of (expanded_key, expanded_value) where:
            - expanded_key: Tensor of shape [B, q_num_heads, kv_S, E]
            - expanded_value: Tensor of shape [B, q_num_heads, kv_S, E]
    """

    if not (
        query.shape[1] > key.shape[1] == value.shape[1]
        and query.shape[1] % key.shape[1] == 0
    ):
        raise AssertionError(
            "SDPA (GQA or MQA) requires q_num_heads > kv_num_heads & "
            "q_num_heads % kv_num_heads == 0"
        )

    # NOTE: QKV are expected to be 4D tensors

    batch_size = op.Shape(query, start=0, end=1)  # [B]
    q_num_heads = op.Shape(query, start=1, end=2)  # [Hq]
    kv_num_heads = op.Shape(key, start=1, end=2)  # [Hk]
    qk_head_size = op.Shape(key, start=3, end=4)  # [Dk]
    v_head_size = op.Shape(value, start=3, end=4)  # [Dv]
    new_kv_seq_len = op.Shape(key, start=2, end=3)  # [T]

    interleave_dim = op.Div(q_num_heads, kv_num_heads)  # Hq / Hk
    two = op.Constant(value_int=2)
    k_unsqueezed = op.Unsqueeze(key, two)  # [B, Hk, 1, T, Dk]
    v_unsqueezed = op.Unsqueeze(value, two)  # [B, Hv, 1, T, Dv]

    k_expand_shape = op.Concat(
        batch_size, kv_num_heads, interleave_dim, new_kv_seq_len, qk_head_size, axis=0
    )
    k_expand = op.Expand(k_unsqueezed, k_expand_shape)
    v_expand_shape = op.Concat(
        batch_size, kv_num_heads, interleave_dim, new_kv_seq_len, v_head_size, axis=0
    )
    v_expand = op.Expand(v_unsqueezed, v_expand_shape)

    k_attention_shape = op.Concat(
        batch_size, q_num_heads, new_kv_seq_len, qk_head_size, axis=0
    )
    v_attention_shape = op.Concat(
        batch_size, q_num_heads, new_kv_seq_len, v_head_size, axis=0
    )

    expanded_key = op.Reshape(k_expand, k_attention_shape)
    expanded_value = op.Reshape(v_expand, v_attention_shape)

    return expanded_key, expanded_value

