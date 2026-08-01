
def _make_scalar_type(np_scalar_type: type) -> _ScalarMeta:
  meta = _ScalarMeta(np_scalar_type.__name__, (object,),
                     {"dtype": np.dtype(np_scalar_type)})
  meta.__module__ = _PUBLIC_MODULE_NAME
  meta.__doc__ =\
  f"""A JAX scalar constructor of type {np_scalar_type.__name__}.

  While NumPy defines scalar types for each data type, JAX represents
  scalars as zero-dimensional arrays.
  """
  return meta

