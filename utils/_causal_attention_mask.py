
def _causal_attention_mask(
    g: jit_utils.GraphContext, query: torch._C.Value, key: torch._C.Value
) -> torch._C.Value:
    """Create a causal mask for the given query and key tensors.

    Equivalent to::
        mask = torch.ones(L, S, dtype=torch.bool).tril(diagonal=0)
        attn_mask = torch.zeros(L, S, dtype=torch.float)
        attn_mask = attn_mask.masked_fill(not mask, -float("inf"))

    Args:
        query: Tensor of shape [..., L, E]
        key: Tensor of shape [..., S, E]

    Returns:
        Tensor of shape [L, S]
    """

    query_shape = g.op("Shape", query)
    key_shape = g.op("Shape", key)

    last_idx = g.op("Constant", value_t=torch.tensor([-1], dtype=torch.int64))
    second_last_idx = g.op("Constant", value_t=torch.tensor([-2], dtype=torch.int64))
    target_length = g.op("Slice", query_shape, second_last_idx, last_idx)
    source_length = g.op("Slice", key_shape, second_last_idx, last_idx)
    # attn_mask = torch.ones(L, S) := {
    size = g.op("Concat", target_length, source_length, axis_i=0)
    const_one = g.op("Constant", value_t=torch.tensor([1.0]))
    attn_mask = g.op("Expand", const_one, size)
    # }
    attn_mask = g.op("Trilu", attn_mask, upper_i=0)
    # The causal mask has 0s in the lower triangle and -inf in the upper triangle.
    const_zero = g.op("Constant", value_t=torch.tensor([0.0]))
    const_neg_inf = g.op("Constant", value_t=torch.tensor([-float("inf")]))
    attn_mask = g.op(
        "Where", g.op("Equal", attn_mask, const_zero), const_neg_inf, const_zero
    )
    return attn_mask


def _causal_attention_mask(query: TFloat, key: TFloat, op: Opset) -> TFloat:
    """Create a causal mask for the given query and key tensors.

    Equivalent to::
        mask = torch.ones(L, S, dtype=torch.bool).tril(diagonal=0)
        attn_mask = torch.zeros(L, S, dtype=torch.float)
        attn_mask = attn_mask.masked_fill(not mask, -float("inf"))

    Args:
        query: Tensor of shape [..., L, E]
        key: Tensor of shape [..., S, E]

    Returns:
        Tensor of shape [L, S]
    """
    q_shape = op.Shape(query)
    k_shape = op.Shape(key)

    target_length = op.Slice(
        q_shape, op.Constant(value_ints=[-2]), op.Constant(value_ints=[-1])
    )
    source_length = op.Slice(
        k_shape, op.Constant(value_ints=[-2]), op.Constant(value_ints=[-1])
    )
    # attn_mask = torch.ones(L, S) := {
    size = op.Concat(target_length, source_length, axis=0)
    attn_mask = op.Expand(op.Constant(value_float=1.0), size)
    # }
    attn_mask = op.Trilu(attn_mask, upper=0)
    # The causal mask has 0s in the lower triangle and -inf in the upper triangle.
    attn_mask = op.Where(
        op.Equal(attn_mask, op.Constant(value_float=0.0)),
        op.Constant(value_float=-float("inf")),
        op.Constant(value_float=0.0),
    )
    attn_mask = op.CastLike(attn_mask, query)
    return attn_mask

