
def jax_dtype(obj: DTypeLike | None, *, align: bool = False,
              copy: bool = False) -> DType:
  """Cast an object to a dtype, respecting JAX dtype defaults.

  Arguments mirror those of :func:`numpy.dtype`.
  """
  if obj is None:
    obj = default_float_dtype()
  elif issubdtype(obj, extended):
    return obj  # pyrefly: ignore[bad-return]
  elif isinstance(obj, type) and (f := _DEFAULT_TYPEMAP.get(obj)) is not None:
    obj = f()
  return np.dtype(obj, align=align, copy=copy)

