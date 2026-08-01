
def _maybe_cast_reduce_op_input(g: jit_utils.GraphContext, self):
    scalar_type = _type_utils.JitScalarType.from_value(
        self, _type_utils.JitScalarType.UNDEFINED
    )
    if scalar_type != _type_utils.JitScalarType.UNDEFINED:
        # This check only covers traced modules where dtype is present
        # pytorch reduce-ops cast all other integral types to int64
        if not _is_fp(self) and scalar_type != _type_utils.JitScalarType.INT64:
            self = g.op("Cast", self, to_i=_C_onnx.TensorProtoDataType.INT64)
    return self

