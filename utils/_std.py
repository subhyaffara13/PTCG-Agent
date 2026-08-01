
def _std(a, axis=None, dtype=None, out=None, ddof=0, keepdims=False, *,
         where=True, mean=None):
    ret = _var(a, axis=axis, dtype=dtype, out=out, ddof=ddof,
               keepdims=keepdims, where=where, mean=mean)

    if isinstance(ret, mu.ndarray):
        ret = um.sqrt(ret, out=ret)
    elif hasattr(ret, 'dtype'):
        ret = ret.dtype.type(um.sqrt(ret))
    else:
        ret = um.sqrt(ret)

    return ret


def _std(a, **args):
    return a.std(**args)


def _std(self: Array, axis: reductions.Axis = None, dtype: DTypeLike | None = None,
         out: None = None, ddof: int = 0, keepdims: bool = False, *,
         where: ArrayLike | None = None, correction: int | float | None = None) -> Array:
  """Compute the standard deviation along a given axis.

  Refer to :func:`jax.numpy.std` for full documentation.
  """
  return reductions.std(self, axis=axis, dtype=dtype, out=out, ddof=ddof, keepdims=keepdims,
                        where=where, correction=correction)


def _std(a: Array, *, axis: Axis = None, dtype: DTypeLike | None = None,
         out: None = None, correction: int | float = 0, keepdims: bool = False,
         where: ArrayLike | None = None, mean: ArrayLike | None = None) -> Array:
  where = check_where("std", where)
  if dtype is not None:
    dtype = dtypes.check_and_canonicalize_user_dtype(dtype, "std")
    if not dtypes.issubdtype(dtype, np.inexact):
      raise ValueError(f"dtype argument to jnp.std must be inexact; got {dtype}")
  if out is not None:
    raise NotImplementedError("The 'out' argument to jnp.std is not supported.")
  return lax.sqrt(var(a, axis=axis, dtype=dtype, correction=correction,
                      keepdims=keepdims, where=where, mean=mean))

