
def scalar_type_to_dtype(typ: type, value: Any = None) -> DType:
  """Return the numpy dtype for the given scalar type.

  Raises
  ------
  OverflowError: if `typ` is `int` and the value is too large for int64.

  Examples
  --------
  >>> scalar_type_to_dtype(int)
  dtype('int32')
  >>> scalar_type_to_dtype(float)
  dtype('float32')
  >>> scalar_type_to_dtype(complex)
  dtype('complex64')
  >>> scalar_type_to_dtype(int)
  dtype('int32')
  >>> scalar_type_to_dtype(int, 0)
  dtype('int32')
  >>> scalar_type_to_dtype(int, 1 << 63)  # doctest: +IGNORE_EXCEPTION_DETAIL
  Traceback (most recent call last):
  OverflowError: Python int 9223372036854775808 too large to convert to int32
  """
  dtype = canonicalize_dtype(python_scalar_types_to_dtypes[typ])
  if typ is int and value is not None:
    iinfo = np.iinfo(dtype)
    if value < iinfo.min or value > iinfo.max:
      raise OverflowError(f"Python int {value} too large to convert to {dtype}")
  return dtype

