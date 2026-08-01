
def _select_helper(g: jit_utils.GraphContext, self, dim, index, apply_reshape=True):
    index_const = _maybe_get_scalar(index)
    index_dim = _get_tensor_rank(index)
    if not _is_value(index_const):
        # Index is a constant scalar. Make it a size 1 constant tensor.
        index = g.op("Constant", value_t=torch.LongTensor([index_const]))
    elif index_dim is not None and apply_reshape:
        if index_dim == 0:
            # Index is a scalar. Reshape it to a size 1 tensor.
            index = _reshape_helper(
                g, index, g.op("Constant", value_t=torch.LongTensor([1]))
            )

    index_scalar_type = _type_utils.JitScalarType.from_value(
        index, _type_utils.JitScalarType.UNDEFINED
    )
    if index_scalar_type not in {
        _type_utils.JitScalarType.INT64,
        _type_utils.JitScalarType.INT,
    }:
        index = g.op("Cast", index, to_i=_C_onnx.TensorProtoDataType.INT64)
    return g.op("Gather", self, index, axis_i=dim)

