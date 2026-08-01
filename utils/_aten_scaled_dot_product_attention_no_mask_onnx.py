
def _aten_scaled_dot_product_attention_no_mask_onnx(
    query: TFloat,
    key: TFloat,
    value: TFloat,
    scale: TFloat,
    dropout_p: float,
    op: Opset,
) -> TFloat:
    # Swap the last two axes of key
    key_last_dim = op.Shape(key, start=-1)
    key_second_last_dim = op.Shape(key, start=-2, end=-1)
    key_first_dims = op.Shape(key, end=-2)
    # Contract the dimensions that are not the last two so we can transpose
    # with a static permutation.
    key_squeezed_shape = op.Concat(
        op.Constant(value_ints=[-1]), key_second_last_dim, key_last_dim, axis=0
    )
    key_squeezed = op.Reshape(key, key_squeezed_shape)
    key_squeezed_transposed = op.Transpose(key_squeezed, perm=[0, 2, 1])
    key_transposed_shape = op.Concat(
        key_first_dims, key_last_dim, key_second_last_dim, axis=0
    )
    key_transposed = op.Reshape(key_squeezed_transposed, key_transposed_shape)

    # https://github.com/pytorch/pytorch/blob/12da0c70378b5be9135c6fda62a9863bce4a4818/aten/src/ATen/native/transformers/attention.cpp#L653
    # Scale q, k before matmul for stability see https://tinyurl.com/sudb9s96 for math
    query_scaled = op.Mul(query, op.Sqrt(scale))
    key_transposed_scaled = op.Mul(
        key_transposed, op.CastLike(op.Sqrt(scale), key_transposed)
    )
    attn_weight = op.Softmax(
        op.MatMul(query_scaled, key_transposed_scaled),
        axis=-1,
    )
    attn_weight, _ = op.Dropout(attn_weight, dropout_p)
    return op.MatMul(attn_weight, value)

