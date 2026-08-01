
def _all(g: jit_utils.GraphContext, *args):
    input = g.op("Not", args[0])
    # aten::all(Tensor self)
    if len(args) == 1:
        return g.op("Not", _any(g, input))
    # aten::all(Tensor self, int[]? dim, bool keepdim)
    else:
        return g.op("Not", _any(g, input, args[1], args[2]))


def _all(a, axis=None, dtype=None, out=None, keepdims=False, *, where=True):
    # By default, return a boolean for any and all
    if dtype is None:
        dtype = bool_dt
    # Parsing keyword arguments is currently fairly slow, so avoid it for now
    if where is True:
        return umr_all(a, axis, dtype, out, keepdims)
    return umr_all(a, axis, dtype, out, keepdims, where=where)


def _all(self: Array, axis: reductions.Axis = None, out: None = None,
         keepdims: bool = False, *, where: ArrayLike | None = None) -> Array:
  """Test whether all array elements along a given axis evaluate to True.

  Refer to :func:`jax.numpy.all` for the full documentation.
  """
  return reductions.all(self, axis=axis, out=out, keepdims=keepdims, where=where)

