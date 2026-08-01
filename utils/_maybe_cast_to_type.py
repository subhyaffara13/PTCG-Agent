
def _maybe_cast_to_type(
    g: jit_utils.GraphContext, value, jit_type: _type_utils.JitScalarType
):
    if (
        _type_utils.JitScalarType.from_value(value, _type_utils.JitScalarType.UNDEFINED)
        != jit_type
    ):
        return g.op(
            "Cast",
            value,
            to_i=jit_type.onnx_type(),
        )
    return value

