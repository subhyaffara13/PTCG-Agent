from typing import Any, Tuple

def _transpose(x: ArrayType, axes: Tuple[int, ...], backend: str = "numpy") -> ArrayType:
    """Base transpose."""
    fn = backends.get_func("transpose", backend, _default_transpose)
    return fn(x, axes)


def _transpose(matrix_of_tensors):
    # returns list of tuples
    return list(zip(*matrix_of_tensors))


def _transpose(self: Array, *args: Any) -> Array:
  """Returns a copy of the array with axes transposed.

  Refer to :func:`jax.numpy.transpose` for full documentation.
  """
  if not args:
    axis = None
  elif len(args) == 1:
    axis = args[0] if args[0] is None else _ensure_index_tuple(args[0])
  else:
    axis = _ensure_index_tuple(args)
  return lax_numpy.transpose(self, axis)


def _transpose(xs):
  return tuple(zip(*xs))

