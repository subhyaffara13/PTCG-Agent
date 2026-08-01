
def _attention_scale(
    g: jit_utils.GraphContext, query: torch._C.Value
) -> torch._C.Value:
    """Calculate the scale factor for the attention result.

    Args:
        query: Tensor of shape [..., L, E]

    Returns:
        Scalar scale factor := 1 / math.sqrt(query.size(-1))
    """
    query_shape = g.op("Shape", query)
    query_shape_last = g.op(
        "Slice",
        query_shape,
        g.op("Constant", value_t=torch.tensor([-1], dtype=torch.int64)),
        g.op(
            "Constant", value_t=torch.tensor([_constants.INT64_MAX], dtype=torch.int64)
        ),
    )
    embedding_size = g.op(
        "Cast",
        query_shape_last,
        to_i=_type_utils.JitScalarType.from_value(query).onnx_type(),
    )
    const_one = g.op("Constant", value_t=torch.tensor([1.0], dtype=torch.float))
    scale = g.op("Div", const_one, g.op("Sqrt", embedding_size))
    # Add a Cast to convert the scale back to original type
    scale = g.op(
        "Cast",
        scale,
        to_i=_type_utils.JitScalarType.from_value(query).onnx_type(),
    )
    return scale


def _attention_scale(query: TFloat, op: Opset) -> TFloat:
    """Calculate the scale factor for the attention result.

    Args:
        query: Tensor of shape [..., L, E]

    Returns:
        Scalar scale factor := 1 / math.sqrt(query.size(-1))
    """
    q_shape = op.Shape(query)
    q_last_dim = op.Gather(q_shape, op.Constant(value_ints=[-1]))
    embedding_size = op.CastLike(q_last_dim, query)
    one = op.Constant(value_float=1.0)
    cast_one = op.CastLike(one, query)
    scale = op.Div(cast_one, op.Sqrt(embedding_size))
    return scale

