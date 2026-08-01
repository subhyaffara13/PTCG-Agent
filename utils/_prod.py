
def _prod(xs: Iterable[int]) -> int:
    """Compute product of a list"""
    prod = 1
    for x in xs:
        prod *= x
    return prod


def _prod(seq):
    """Returns the product of the elements in the sequence `seq`."""
    p = 1
    for elem in seq:
        p *= elem
    return p


def _prod(a):
    p = 1
    for x in a:
        p *= x
    return p


def _prod(a, axis=None, dtype=None, out=None, keepdims=False,
          initial=_NoValue, where=True):
    return umr_prod(a, axis, dtype, out, keepdims, initial, where)


def _prod(self: Array, axis: reductions.Axis = None, dtype: DTypeLike | None = None,
          out: None = None, keepdims: bool = False,
          initial: ArrayLike | None = None, where: ArrayLike | None = None,
          promote_integers: bool = True) -> Array:
  """Return product of the array elements over a given axis.

  Refer to :func:`jax.numpy.prod` for the full documentation.
  """
  return reductions.prod(self, axis=axis, dtype=dtype, out=out, keepdims=keepdims,
                         initial=initial, where=where, promote_integers=promote_integers)

