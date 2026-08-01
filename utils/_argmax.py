
def _argmax(x):
    return np.flatnonzero(x >= np.max(x))


def _argmax(self: Array, axis: int | None = None, out: None = None,
            keepdims: bool | None = None) -> Array:
  """Return the index of the maximum value.

  Refer to :func:`jax.numpy.argmax` for the full documentation.
  """
  return lax_numpy.argmax(self, axis=axis, out=out, keepdims=keepdims)


def _argmax(a: Array, axis: int | None = None, keepdims: bool = False) -> Array:
  if axis is None:
    dims = list(range(np.ndim(a)))
    a = ravel(a)
    axis = 0
  else:
    dims = [axis]
  if a.shape[axis] == 0:
    raise ValueError("attempt to get argmax of an empty sequence")
  # TODO(phawkins): use an int64 index if the dimension is large enough.
  result = lax.argmax(a, _canonicalize_axis(axis, a.ndim), int)
  return expand_dims(result, dims) if keepdims else result

