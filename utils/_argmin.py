
def _argmin(x):
    return np.flatnonzero(x <= np.min(x))


def _argmin(self: Array, axis: int | None = None, out: None = None,
            keepdims: bool | None = None) -> Array:
  """Return the index of the minimum value.

  Refer to :func:`jax.numpy.argmin` for the full documentation.
  """
  return lax_numpy.argmin(self, axis=axis, out=out, keepdims=keepdims)


def _argmin(a: Array, axis: int | None = None, keepdims: bool = False) -> Array:
  if axis is None:
    dims = list(range(np.ndim(a)))
    a = ravel(a)
    axis = 0
  else:
    dims = [axis]
  if a.shape[axis] == 0:
    raise ValueError("attempt to get argmin of an empty sequence")
  # TODO(phawkins): use an int64 index if the dimension is large enough.
  result = lax.argmin(a, _canonicalize_axis(axis, a.ndim), int)
  return expand_dims(result, dims) if keepdims else result

