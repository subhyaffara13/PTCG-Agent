
def is_complex_value(x: _C.Value) -> bool:
    if not _is_value(x):
        raise AssertionError("Expected a Value")
    return _type_utils.JitScalarType.from_value(
        x, _type_utils.JitScalarType.UNDEFINED
    ) in {
        _type_utils.JitScalarType.COMPLEX32,
        _type_utils.JitScalarType.COMPLEX64,
        _type_utils.JitScalarType.COMPLEX128,
    }

