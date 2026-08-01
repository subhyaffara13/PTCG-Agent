
def check_valid_dtype(dtype: DType) -> None:
  if dtype not in _jax_dtype_set:
    raise TypeError(f"Dtype {dtype} is not a valid JAX array "
                    "type. Only arrays of numeric types are supported by JAX.")

