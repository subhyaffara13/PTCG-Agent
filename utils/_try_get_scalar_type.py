
def _try_get_scalar_type(*args) -> _type_utils.JitScalarType | None:
    for arg in args:
        scalar_type = _type_utils.JitScalarType.from_value(
            arg, _type_utils.JitScalarType.UNDEFINED
        )
        if scalar_type != _type_utils.JitScalarType.UNDEFINED:
            return scalar_type
    return None

