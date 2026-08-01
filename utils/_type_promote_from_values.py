
def _type_promote_from_values(*args) -> _type_utils.JitScalarType:
    undef = _type_utils.JitScalarType.UNDEFINED
    jit_types = [_try_get_scalar_type(arg) for arg in args]
    if len(jit_types) == 0:
        return undef
    if len(jit_types) == 1:
        return jit_types[0]  # type: ignore[return-value]
    new_dtype = jit_types[0].dtype()  # type: ignore[union-attr]
    for t in jit_types:
        new_dtype = torch.promote_types(new_dtype, t.dtype())  # type: ignore[union-attr]
    return _type_utils.JitScalarType.from_dtype(new_dtype)

