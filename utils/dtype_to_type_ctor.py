
def dtype_to_type_ctor(dtype: torch.dtype) -> Callable[[NumberType], NumberType]:
    """
    Computes the corresponding Python type constructor for the
    given dtype.
    """
    if not isinstance(dtype, torch.dtype):
        raise AssertionError(f"Expected torch.dtype, got {type(dtype)}")

    if dtype is torch.bool:
        return lambda x: bool(x)
    if dtype in _integer_dtypes:
        return sym_int
    if dtype.is_floating_point:
        return sym_float
    if dtype in _complex_dtypes:
        # TODO: type error here is real, replace with sym_complex
        return lambda x: complex(x)  # type: ignore[arg-type]

    raise ValueError("Invalid dtype!")

