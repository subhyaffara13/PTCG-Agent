
def _min(*args, **kwargs):
    if "key" not in kwargs:
        kwargs["key"] = default_sort_key
    return min(*args, **kwargs)


def _min(self: Array, axis: reductions.Axis = None, out: None = None,
         keepdims: bool = False, initial: ArrayLike | None = None,
         where: ArrayLike | None = None) -> Array:
  """Return the minimum of array elements along a given axis.

  Refer to :func:`jax.numpy.min` for the full documentation.
  """
  return reductions.min(self, axis=axis, out=out, keepdims=keepdims,
                        initial=initial, where=where)

