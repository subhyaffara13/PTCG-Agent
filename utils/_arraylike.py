
def _arraylike(x: ArrayLike) -> bool:
  return (isinstance(x, _arraylike_types) or
          getattr(x, '__jax_array__', None) is not None or np.isscalar(x))

