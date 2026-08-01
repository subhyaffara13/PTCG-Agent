
def _try_cast_integer_to_float(g: jit_utils.GraphContext, *args):
    floating_scalar_types = {
        _type_utils.JitScalarType.HALF,
        _type_utils.JitScalarType.FLOAT,
        _type_utils.JitScalarType.DOUBLE,
    }
    old_type = None
    # Cast the input tensor to Float if its scalarType is known and is not floating number.
    # If casting is performed, return the old scalarType, otherwise return None.
    arg0_type = _type_utils.JitScalarType.from_value(
        args[0], _type_utils.JitScalarType.UNDEFINED
    )
    if arg0_type != _type_utils.JitScalarType.UNDEFINED:
        old_type = arg0_type
        if old_type not in floating_scalar_types:
            old_type = old_type.scalar_name()  # type: ignore[assignment]
            args = tuple(
                g.op("Cast", arg, to_i=_C_onnx.TensorProtoDataType.FLOAT)
                for arg in args
            )
        else:
            return (None,) + args
    else:
        warnings.warn(
            "Only floating datatype is supported for these operators: "
            "{Greater, Less, MatMul, PRelu, Gemm, Flatten}. This might cause "
            "the onnx model to be incorrect, if inputs have integer datatypes.",
            stacklevel=2,
        )
    return (old_type,) + args

