
def _mean(num_microbatches: int) -> Accumulator:
  """An Accumulator that computes the mean of microbatched outputs."""
  if num_microbatches <= 0:
    raise ValueError(f'{num_microbatches=} must be positive.')
  return _lift(
      Accumulator(
          init=_with_floating_check(jnp.zeros_like),
          update=lambda carry, value, _: carry + value,
          finalize=lambda carry: carry / num_microbatches,
          aggregate=functools.partial(jnp.mean, axis=0),
      )
  )


def _mean(a, axis=None, dtype=None, out=None, keepdims=False, *, where=True):
    arr = asanyarray(a)

    is_float16_result = False

    rcount = _count_reduce_items(arr, axis, keepdims=keepdims, where=where)
    if rcount == 0 if where is True else umr_any(rcount == 0, axis=None):
        warnings.warn("Mean of empty slice", RuntimeWarning, stacklevel=2)

    # Cast bool, unsigned int, and int to float64 by default
    if dtype is None:
        if issubclass(arr.dtype.type, (nt.integer, nt.bool)):
            dtype = mu.dtype('f8')
        elif issubclass(arr.dtype.type, nt.float16):
            dtype = mu.dtype('f4')
            is_float16_result = True

    ret = umr_sum(arr, axis, dtype, out, keepdims, where=where)
    if isinstance(ret, mu.ndarray):
        ret = um.true_divide(
                ret, rcount, out=ret, casting='unsafe', subok=False)
        if is_float16_result and out is None:
            ret = arr.dtype.type(ret)
    elif hasattr(ret, 'dtype'):
        if is_float16_result:
            ret = arr.dtype.type(ret / rcount)
        else:
            ret = ret.dtype.type(ret / rcount)
    else:
        ret = ret / rcount

    return ret


def _mean(a, **args):
    return a.mean(**args)


def _mean(self: Array, axis: reductions.Axis = None, dtype: DTypeLike | None = None,
          out: None = None, keepdims: bool = False, *,
          where: ArrayLike | None = None) -> Array:
  """Return the mean of array elements along a given axis.

  Refer to :func:`jax.numpy.mean` for the full documentation.
  """
  return reductions.mean(self, axis=axis, dtype=dtype, out=out,
                         keepdims=keepdims, where=where)


def _mean(a: ArrayLike, axis: Axis = None, dtype: DTypeLike | None = None,
          out: None = None, keepdims: bool = False, *,
          upcast_f16_for_computation: bool = True,
          where: ArrayLike | None = None) -> Array:
  a = ensure_arraylike("mean", a)
  where = check_where("mean", where)
  if out is not None:
    raise NotImplementedError("The 'out' argument to jnp.mean is not supported.")

  if dtype is None:
    result_dtype = dtypes.to_inexact_dtype(a.dtype)
  else:
    result_dtype = dtypes.check_and_canonicalize_user_dtype(dtype, "mean")

  if upcast_f16_for_computation and dtypes.issubdtype(result_dtype, np.inexact):
    computation_dtype = _upcast_f16(result_dtype)
  else:
    computation_dtype = result_dtype

  normalizer = _count(
      a,
      axis=axis,
      keepdims=keepdims,
      where=where,
      dtype=computation_dtype,
  )

  return lax.div(
      sum(a, axis, dtype=computation_dtype, keepdims=keepdims, where=where),
      normalizer,
  ).astype(result_dtype)

