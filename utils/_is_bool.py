
def _is_bool(value) -> bool:
    return (
        _type_utils.JitScalarType.from_value(value, _type_utils.JitScalarType.UNDEFINED)
        == _type_utils.JitScalarType.BOOL
    )

