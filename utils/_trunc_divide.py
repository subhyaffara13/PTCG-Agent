
def _trunc_divide(g: jit_utils.GraphContext, self, other):
    out = g.op("Div", self, other)
    # the correct operation is truncate, which is not supported in ONNX,
    # we cannot call floor since it will behave differently for negative numbers
    # (eg. -0.1 should become -0 )
    # - if scalar_type information are not available, assume that
    # we need to call floor (treat as float)
    out = g.op("Cast", out, to_i=_C_onnx.TensorProtoDataType.INT64)

    # Matching PyTorch's behavior:
    # - if self is fp the output's type is self's type
    # - if self is not fp and other is fp, the output is of type JitScalarType.FLOAT
    # - self is not fp and other is not fp, the output's type is self's output type
    # - the output type defaults to Float
    scalar_type = _type_utils.JitScalarType.from_value(
        self, _type_utils.JitScalarType.UNDEFINED
    )
    if scalar_type != _type_utils.JitScalarType.UNDEFINED:
        if not symbolic_helper._is_fp(self) and symbolic_helper._is_fp(other):
            out = g.op("Cast", out, to_i=_C_onnx.TensorProtoDataType.FLOAT)
        else:
            out = g.op(
                "Cast",
                out,
                to_i=scalar_type.onnx_type(),
            )
    else:
        out = g.op("Cast", out, to_i=_C_onnx.TensorProtoDataType.FLOAT)
    return out

