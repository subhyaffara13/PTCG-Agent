
def _ptp(x):
    """Peak-to-peak value of x.

    This implementation avoids the problem of signed integer arrays having a
    peak-to-peak value that cannot be represented with the array's data type.
    This function returns an unsigned value for signed integer arrays.
    """
    return _unsigned_subtract(x.max(), x.min())


def _ptp(a, axis=None, out=None, keepdims=False):
    return um.subtract(
        umr_maximum(a, axis, None, out, keepdims),
        umr_minimum(a, axis, None, None, keepdims),
        out
    )


def _ptp(self: Array, axis: reductions.Axis = None, out: None = None,
         keepdims: bool = False) -> Array:
  """Return the peak-to-peak range along a given axis.

  Refer to :func:`jax.numpy.ptp` for the full documentation.
  """
  return reductions.ptp(self, axis=axis, out=out, keepdims=keepdims)


def _ptp(a: Array, axis: Axis = None, out: None = None,
         keepdims: bool = False) -> Array:
  if out is not None:
    raise NotImplementedError("The 'out' argument to jnp.ptp is not supported.")
  x = amax(a, axis=axis, keepdims=keepdims)
  y = amin(a, axis=axis, keepdims=keepdims)
  return lax.sub(x, y)

