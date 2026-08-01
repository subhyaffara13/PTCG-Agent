
def _logsumexp(g: jit_utils.GraphContext, input, dim, keepdim):
    if dim is None:
        return g.op("ReduceLogSumExp", input, keepdims_i=0)
    else:
        axes = g.op("Constant", value_t=torch.tensor(dim, dtype=torch.long))
        return g.op("ReduceLogSumExp", input, axes, keepdims_i=keepdim)


def _logsumexp(a, b, *, axis, return_sign, xp):
    # This has been around for about a decade, so let's consider it a feature:
    # Even if element of `a` is infinite or NaN, it adds nothing to the sum if
    # the corresponding weight is zero.
    if b is not None:
        a = xpx.at(a, b == 0).set(-xp.inf, copy=True)

    # Find element with maximum real part, since this is what affects the magnitude
    # of the exponential. Possible enhancement: include log of `b` magnitude in `a`.
    a_max, i_max = _elements_and_indices_with_max_real(a, axis=axis, xp=xp)

    # for precision, these terms are separated out of the main sum.
    a = xpx.at(a, i_max).set(-xp.inf, copy=True if b is None else None)
    i_max_dt = xp.astype(i_max, a.dtype)
    # This is an inefficient way of getting `m` because it is the sum of a sparse
    # array; however, this is the simplest way I can think of to get the right shape.
    b_i_max = i_max_dt if b is None else b * i_max_dt
    m = xp.sum(b_i_max, axis=axis, keepdims=True, dtype=a.dtype)

    # Shift, exponentiate, scale, and sum
    exp = b * xp.exp(a - a_max) if b is not None else xp.exp(a - a_max)
    s = xp.sum(exp, axis=axis, keepdims=True, dtype=exp.dtype)
    s = xp.where(s == 0, s, s/m)

    # Separate sign/magnitude information
    # Originally, this was only performed if `return_sign=True`.
    # However, this is also needed if any elements of `m < 0` or `s < -1`.
    # An improvement would be to perform the calculations only on these entries.

    sgn = xp.sign(s + 1) * xp.sign(m)

    if xp.isdtype(s.dtype, "real floating"):
        # The log functions need positive arguments
        s = xp.where(s < -1, -s - 2, s)
        m = xp.abs(m)
    else:
        # `a_max` can have a sign component for complex input
        sgn = sgn * xp.exp(xp.imag(a_max) * 1.0j)

    # Take log and undo shift
    out = xp.log1p(s) + xp.log(m) + a_max

    if return_sign:
        out = xp.real(out)
    elif xp.isdtype(out.dtype, 'real floating'):
        out = xpx.at(out)[sgn < 0].set(xp.nan)

    return out, sgn


def _logsumexp(a: ArrayLike, axis: Axis = None, dtype: DTypeLike | None = None,
               out: None = None, keepdims: bool = False,
               initial: ArrayLike | None = None, where: ArrayLike | None = None) -> Array:
  """Compute log(sum(exp(a))) while avoiding precision loss."""
  if out is not None:
    raise NotImplementedError("The 'out' argument to jnp.logaddexp.reduce is not supported.")
  if dtype is not None:
    dtype = dtypes.check_and_canonicalize_user_dtype(dtype, "jnp.logaddexp.reduce")
  # TODO(phawkins): dtype isn't used here. That seems like a bug!
  del dtype
  a = ensure_arraylike("logsumexp", a)
  where = check_where("logsumexp", where)
  a_arr, = promote_dtypes_inexact(a)
  pos_dims, dims = _reduction_dims(a_arr, axis)
  amax = max(a_arr.real, axis=dims, keepdims=keepdims, where=where, initial=-np.inf)
  amax = lax.stop_gradient(lax.select(lax.is_finite(amax), amax, lax.full_like(amax, 0)))
  amax_with_dims = amax if keepdims else lax.expand_dims(amax, pos_dims)
  exp_a = lax.exp(lax.sub(a_arr, amax_with_dims.astype(a_arr.dtype)))
  sumexp = exp_a.sum(axis=dims, keepdims=keepdims, where=where)
  result = lax.add(lax.log(sumexp), amax.astype(sumexp.dtype))
  return result if initial is None else lax_other.logaddexp(initial, result)

