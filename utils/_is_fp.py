
def _is_fp(value) -> bool:
    return _type_utils.JitScalarType.from_value(
        value, _type_utils.JitScalarType.UNDEFINED
    ) in {
        _type_utils.JitScalarType.FLOAT,
        _type_utils.JitScalarType.DOUBLE,
        _type_utils.JitScalarType.HALF,
        _type_utils.JitScalarType.BFLOAT16,
    }

