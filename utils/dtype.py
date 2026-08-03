from typing import Any

def dtype(arg):
    if arg is None:
        arg = _dtypes_impl.default_dtypes().float_dtype
    return DType(arg)


def dtype():
    """A fixture providing the ExtensionDtype to validate."""
    raise NotImplementedError


def dtype(request):
    return ArrowDtype(pyarrow_dtype=request.param)


def dtype():
    return CategoricalDtype()


def dtype():
    return DatetimeTZDtype(unit="ns", tz="US/Central")


def dtype():
    return IntervalDtype()


def dtype(request):
    return request.param()


def dtype(request):
    return NumpyEADtype(np.dtype(request.param))


def dtype(request):
    return PeriodDtype(freq=request.param)


def dtype():
    return SparseDtype()


def dtype(string_dtype_arguments):
    storage, na_value = string_dtype_arguments
    return StringDtype(storage=storage, na_value=na_value)


def dtype(request):
    return request.param


def dtype():
    return DecimalDtype()


def dtype():
    return JSONDtype()


def dtype():
    return ListDtype()


def dtype():
    """Fixture returning BooleanDtype"""
    return pd.BooleanDtype()


def dtype(request):
    """Parametrized fixture returning a float 'dtype'"""
    return request.param()


def dtype(request):
    """Parametrized fixture returning integer 'dtype'"""
    return request.param()


def dtype(string_dtype_arguments):
    """Fixture giving StringDtype from parametrized storage and na_value arguments"""
    storage, na_value = string_dtype_arguments
    return pd.StringDtype(storage=storage, na_value=na_value)


def dtype(na_object, coerce):
    """Cartesian project of missing data sentinel and string coercion options"""
    return get_dtype(na_object, coerce)


def dtype(x: Any) -> DType:
  """Return the dtype object for a value or type.

  Python scalars, Python scalar types, NumPy scalar type, NumPy dtypes, and
  non-JAX arrays will have their dtypes canonicalized.

  Note: this is not the same function as jax.numpy.dtype, which simply aliases
  numpy.dtype."""
  # TODO(phawkins): in the future, we would like to:
  # - return the default dtype for Python scalar types and values
  # - canonicalize NumPy array and scalar types
  # - return NumPy dtypes as-is, uncanonicalized.
  if x is None:
    raise ValueError(f"Invalid argument to dtype: {x}.")
  if isinstance(x, type):
    # Python scalar types, e.g., int, float
    if (dt := python_scalar_types_to_dtypes.get(x)) is not None:
      return canonicalize_dtype(dt)

    # Numpy scalar types, e.g., np.int32, np.float32
    if _issubclass(x, np.generic):
      dt = np.dtype(x)
      return _maybe_canonicalize_explicit_dtype(dt, "dtype")

  # Python scalar values, e.g., int(3), float(3.14)
  elif (dt := python_scalar_types_to_dtypes.get(type(x))) is not None:
    return canonicalize_dtype(dt)
  # Jax Arrays, literal arrays, and scalars.
  # We intentionally do not canonicalize these types: once we've formed an x64
  # value, that is something we respect irrespective of the x64 mode.
  elif isinstance(x, _types_whose_dtype_should_not_be_canonicalized):
    return x.dtype

  if isinstance(x, (str, np.dtype)):
    dt = np.dtype(x)
    if dt not in _jax_dtype_set and not issubdtype(dt, extended):
      raise TypeError(f"Value '{x}' with dtype {dt} is not a valid JAX array "
                      "type. Only arrays of numeric types are supported by JAX.")
    return _maybe_canonicalize_explicit_dtype(dt, "dtype")

  # If x has a dtype attribute, and it's a valid dtype, use it. This avoids
  # calling np.result_type on objects that might have a .dtype but are not
  # standard NumPy array-like, which can lead to warnings in NumPy 2.4+.
  dt_attr = getattr(x, 'dtype', None)
  if issubdtype(dt_attr, extended) or isinstance(dt_attr, np.dtype):
    dt = dt_attr
  else:
    try:
      dt = np.result_type(x)
    except TypeError as err:
      raise TypeError(f"Cannot determine dtype of {x}") from err
  if dt not in _jax_dtype_set and not issubdtype(dt, extended):
    raise TypeError(f"Value '{x}' with dtype {dt} is not a valid JAX array "
                    "type. Only arrays of numeric types are supported by JAX.")
  # TODO(jakevdp): fix return type annotation and remove this ignore.
  return canonicalize_dtype(dt, allow_extended_dtype=True)  # pyrefly: ignore[bad-return]

