
def _isscalar(x):
    """Check whether x is if a scalar type, or 0-dim"""
    return np.isscalar(x) or hasattr(x, 'shape') and x.shape == ()


def _isscalar(element: Any) -> bool:
  m = getattr(element, '__jax_array__', None)
  if m is not None:
    element = m()
  return dtypes.is_weakly_typed_scalar(element) or np.isscalar(element)

