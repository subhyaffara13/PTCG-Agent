
def _var(x, axis=0, ddof=0, mean=None, xp=None):
    # Calculate variance of sample, warning if precision is lost
    xp = array_namespace(x) if xp is None else xp
    var = _moment(x, 2, axis, center=mean, xp=xp)
    if ddof != 0:
        n = _count_nonmasked(x, axis, xp=xp)
        n = xp.asarray(n, dtype=x.dtype, device=xp_device(x))
        var *= (n / (n-ddof))  # to avoid error on division by zero
    return var


def _var(a, axis=None, dtype=None, out=None, ddof=0, keepdims=False, *,
         where=True, mean=None):
    arr = asanyarray(a)

    rcount = _count_reduce_items(arr, axis, keepdims=keepdims, where=where)
    # Make this warning show up on top.
    if ddof >= rcount if where is True else umr_any(ddof >= rcount, axis=None):
        warnings.warn("Degrees of freedom <= 0 for slice", RuntimeWarning,
                      stacklevel=2)

    # Cast bool, unsigned int, and int to float64 by default
    if dtype is None and issubclass(arr.dtype.type, (nt.integer, nt.bool)):
        dtype = mu.dtype('f8')

    if mean is not None:
        arrmean = mean
    else:
        # Compute the mean.
        # Note that if dtype is not of inexact type then arraymean will
        # not be either.
        arrmean = umr_sum(arr, axis, dtype, keepdims=True, where=where)
        # The shape of rcount has to match arrmean to not change the shape of
        # out in broadcasting. Otherwise, it cannot be stored back to arrmean.
        if rcount.ndim == 0:
            # fast-path for default case when where is True
            div = rcount
        else:
            # matching rcount to arrmean when where is specified as array
            div = rcount.reshape(arrmean.shape)
        if isinstance(arrmean, mu.ndarray):
            arrmean = um.true_divide(arrmean, div, out=arrmean,
                                     casting='unsafe', subok=False)
        elif hasattr(arrmean, "dtype"):
            arrmean = arrmean.dtype.type(arrmean / rcount)
        else:
            arrmean = arrmean / rcount

    # Compute sum of squared deviations from mean
    # Note that x may not be inexact and that we need it to be an array,
    # not a scalar.
    x = um.subtract(arr, arrmean, out=...)
    if issubclass(arr.dtype.type, (nt.floating, nt.integer)):
        x = um.square(x, out=x)
    # Fast-paths for built-in complex types
    elif (_float_dtype := _complex_to_float.get(x.dtype)) is not None:
        xv = x.view(dtype=(_float_dtype, (2,)))
        um.square(xv, out=xv)
        x = um.add(xv[..., 0], xv[..., 1], out=x.real)
    # Most general case; includes handling object arrays containing imaginary
    # numbers and complex types with non-native byteorder
    else:
        x = um.multiply(x, um.conjugate(x), out=x).real

    ret = umr_sum(x, axis, dtype, out, keepdims=keepdims, where=where)

    # Compute degrees of freedom and make sure it is not negative.
    rcount = um.maximum(rcount - ddof, 0)

    # divide by degrees of freedom
    if isinstance(ret, mu.ndarray):
        ret = um.true_divide(
                ret, rcount, out=ret, casting='unsafe', subok=False)
    elif hasattr(ret, 'dtype'):
        ret = ret.dtype.type(ret / rcount)
    else:
        ret = ret / rcount

    return ret


def _var(a, **args):
    return a.var(**args)


def _var(self: Array, axis: reductions.Axis = None, dtype: DTypeLike | None = None,
         out: None = None, ddof: int = 0, keepdims: bool = False, *,
         where: ArrayLike | None = None, correction: int | float | None = None) -> Array:
  """Compute the variance along a given axis.

  Refer to :func:`jax.numpy.var` for full documentation.
  """
  return reductions.var(self, axis=axis, dtype=dtype, out=out, ddof=ddof,
                        keepdims=keepdims, where=where, correction=correction)


def _var(a: Array, *, axis: Axis = None, dtype: DTypeLike | None = None,
         out: None = None, correction: int | float = 0, keepdims: bool = False,
         where: ArrayLike | None = None, a_mean: ArrayLike | None = None) -> Array:
  where = check_where("var", where)
  if dtype is not None:
    dtype = dtypes.check_and_canonicalize_user_dtype(dtype, "var")
  if out is not None:
    raise NotImplementedError("The 'out' argument to jnp.var is not supported.")

  computation_dtype, dtype = _var_promote_types(a.dtype, dtype)
  a = lax.asarray(a).astype(computation_dtype)
  if a_mean is None:
    a_mean = mean(a, axis, dtype=computation_dtype, keepdims=True, where=where)
  else:
    a_mean = ensure_arraylike("var", a_mean).astype(computation_dtype)

  centered = lax.sub(a, a_mean)
  if dtypes.issubdtype(computation_dtype, np.complexfloating):
    centered = lax.real(lax.mul(centered, lax.conj(centered)))
    computation_dtype = centered.dtype  # avoid casting to complex below.
  else:
    centered = lax.square(centered)

  normalizer = _count(
      a,
      axis=axis,
      keepdims=keepdims,
      where=where,
      dtype=computation_dtype,
  )

  normalizer = lax.sub(normalizer, lax.convert_element_type(correction, computation_dtype))
  result = sum(centered, axis, dtype=computation_dtype, keepdims=keepdims, where=where)
  result = lax.div(result, normalizer).astype(dtype)
  with config.debug_nans(False):
    result = _where(normalizer > 0, result, np.nan)
  return result

