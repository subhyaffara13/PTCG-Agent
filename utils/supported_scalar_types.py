
def supported_scalar_types() -> tuple[type, ...]:
    type_to_torch_dtype = supported_builtin_dtype_torch_dtype()
    return tuple(type_to_torch_dtype.keys())

