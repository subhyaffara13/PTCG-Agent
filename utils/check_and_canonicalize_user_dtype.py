
def check_and_canonicalize_user_dtype(dtype, fun_name=None) -> DType:
  """Checks validity of a user-provided dtype, and returns its canonical form.

  For Python scalar types this function returns the corresponding default dtype.
  """
  if dtype is None:
    raise ValueError("dtype must be specified.")
  if isinstance(dtype, Array):
    raise ValueError("Passing an array as a dtype argument is no longer "
                     "supported; instead of dtype=arr use dtype=arr.dtype.")
  if issubdtype(dtype, extended):
    return dtype
  # Avoid using `dtype in [...]` because of numpy dtype equality overloading.
  if isinstance(dtype, type) and (f := _DEFAULT_TYPEMAP.get(dtype)) is not None:
    return f()
  np_dtype = np.dtype(dtype)
  if np_dtype not in _jax_dtype_set:
    msg = (
        f'JAX only supports number, bool, and string dtypes, got dtype {dtype}'
    )
    msg += f" in {fun_name}" if fun_name else ""
    raise TypeError(msg)
  return _maybe_canonicalize_explicit_dtype(np_dtype, fun_name or "")

