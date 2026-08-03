from typing import Any

def canonicalize_shape(shape: Shape, context: str="") -> tuple[Any, ...]:
  """Canonicalizes and checks for errors in a user-provided shape value.

  Args:
    shape: a Python value that represents a shape.

  Returns:
    A tuple of canonical dimension values.
  """
  if isinstance(shape, int):
    shape = shape,
  try:
    return tuple(unsafe_map(_canonicalize_dimension, shape))
  except TypeError:
    pass
  raise _invalid_shape_error(shape, context)


def canonicalize_shape(shape: Any, context: str="") -> core.Shape:
  if (not isinstance(shape, (tuple, list)) and
      (getattr(shape, 'ndim', None) == 0 or np.ndim(shape) == 0)):
    return core.canonicalize_shape((shape,), context)
  else:
    return core.canonicalize_shape(shape, context)

