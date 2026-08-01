
def logsumexp(
    input: Tensor,
    dim: DimOrDims = None,
    *,
    keepdim: bool = False,
    dtype: DType | None = None,
    mask: Tensor | None = None,
) -> Tensor:
    if dtype is None:
        dtype = input.dtype
    dim_ = _canonical_dim(dim, input.ndim)
    mask_input = _combine_input_and_mask(logsumexp, input, mask)
    if mask_input.layout == torch.strided:
        return torch.logsumexp(mask_input, dim_, keepdim=keepdim).to(dtype=dtype)
    else:
        raise ValueError(
            f"masked logsumexp expects strided tensor (got {mask_input.layout} tensor)"
        )


def logsumexp(
    self: TensorLikeType, dim: DimsType, keepdim: bool = False
) -> TensorLikeType:
    if not isinstance(dim, Iterable):
        dim = (dim,)
    if self.numel() == 0:
        return torch.sum(torch.exp(self), dim, keepdim).log()

    maxes = torch.amax(torch.real(self), dim, keepdim=True)
    maxes = torch.masked_fill(maxes, maxes.abs() == float("inf"), 0)

    maxes_squeezed = maxes if keepdim else torch.squeeze(maxes, dim)

    result = torch.sum(torch.exp(self - maxes), dim, keepdim)
    return result.log().add(maxes_squeezed)


def logsumexp(g: jit_utils.GraphContext, input, dim, keepdim):
    return g.op("ReduceLogSumExp", input, axes_i=dim, keepdims_i=keepdim)


def logsumexp(a, axis=None, b=None, keepdims=False, return_sign=False):
    """Compute the log of the sum of exponentials of input elements.

    Parameters
    ----------
    a : array_like
        Input array.
    axis : None or int or tuple of ints, optional
        Axis or axes over which the sum is taken. By default `axis` is None,
        and all elements are summed.

        .. versionadded:: 0.11.0
    b : array-like, optional
        Scaling factor for exp(`a`) must be of the same shape as `a` or
        broadcastable to `a`. These values may be negative in order to
        implement subtraction.

        .. versionadded:: 0.12.0
    keepdims : bool, optional
        If this is set to True, the axes which are reduced are left in the
        result as dimensions with size one. With this option, the result
        will broadcast correctly against the original array.

        .. versionadded:: 0.15.0
    return_sign : bool, optional
        If this is set to True, the result will be a pair containing sign
        information; if False, results that are negative will be returned
        as NaN. Default is False (no sign information).

        .. versionadded:: 0.16.0

    Returns
    -------
    res : ndarray
        The result, ``np.log(np.sum(np.exp(a)))`` calculated in a numerically
        more stable way. If `b` is given then ``np.log(np.sum(b*np.exp(a)))``
        is returned. If ``return_sign`` is True, ``res`` contains the log of
        the absolute value of the argument.
    sgn : ndarray
        If ``return_sign`` is True, this will be an array of floating-point
        numbers matching res containing +1, 0, -1 (for real-valued inputs)
        or a complex phase (for complex inputs). This gives the sign of the
        argument of the logarithm in ``res``.
        If ``return_sign`` is False, only one result is returned.

    See Also
    --------
    :data:`numpy.logaddexp`
    :data:`numpy.logaddexp2`

    Notes
    -----
    NumPy has a logaddexp function which is very similar to `logsumexp`, but
    only handles two arguments. `logaddexp.reduce` is similar to this
    function, but may be less stable.

    The logarithm is a multivalued function: for each :math:`x` there is an
    infinite number of :math:`z` such that :math:`exp(z) = x`. The convention
    is to return the :math:`z` whose imaginary part lies in :math:`(-pi, pi]`.

    Examples
    --------
    >>> import numpy as np
    >>> from scipy.special import logsumexp
    >>> a = np.arange(10)
    >>> logsumexp(a)
    9.4586297444267107
    >>> np.log(np.sum(np.exp(a)))
    9.4586297444267107

    With weights

    >>> a = np.arange(10)
    >>> b = np.arange(10, 0, -1)
    >>> logsumexp(a, b=b)
    9.9170178533034665
    >>> np.log(np.sum(b*np.exp(a)))
    9.9170178533034647

    Returning a sign flag

    >>> logsumexp([1,2],b=[1,-1],return_sign=True)
    (1.5413248546129181, -1.0)

    Notice that `logsumexp` does not directly support masked arrays. To use it
    on a masked array, convert the mask into zero weights:

    >>> a = np.ma.array([np.log(2), 2, np.log(3)],
    ...                  mask=[False, True, False])
    >>> b = (~a.mask).astype(int)
    >>> logsumexp(a.data, b=b), np.log(5)
    1.6094379124341005, 1.6094379124341005

    """
    xp = array_namespace(a, b)
    a, b = xp_promote(a, b, broadcast=True, force_floating=True, xp=xp)
    a = xpx.atleast_nd(a, ndim=1, xp=xp)
    b = xpx.atleast_nd(b, ndim=1, xp=xp) if b is not None else b
    axis = tuple(range(a.ndim)) if axis is None else axis

    if xp_size(a) != 0:
        with np.errstate(divide='ignore', invalid='ignore', over='ignore'):
            # Where result is infinite, we use the direct logsumexp calculation to
            # delegate edge case handling to the behavior of `xp.log` and `xp.exp`,
            # which should follow the C99 standard for complex values.
            b_exp_a = xp.exp(a) if b is None else b * xp.exp(a)
            sum_ = xp.sum(b_exp_a, axis=axis, keepdims=True)
            sgn_inf = xp.sign(sum_) if return_sign else None
            sum_ = xp.abs(sum_) if return_sign else sum_
            out_inf = xp.log(sum_)

        with np.errstate(divide='ignore', invalid='ignore'):  # log of zero is OK
            out, sgn = _logsumexp(a, b, axis=axis, return_sign=return_sign, xp=xp)

        # Replace infinite results. This probably could be done with an
        # `apply_where`-like strategy to avoid redundant calculation, but currently
        # `apply_where` itself is only for elementwise functions.
        out_finite = xp.isfinite(out)
        out = xp.where(out_finite, out, out_inf)
        sgn = xp.where(out_finite, sgn, sgn_inf) if return_sign else sgn
    else:
        shape = np.asarray(a.shape)  # NumPy is convenient for shape manipulation
        shape[axis] = 1
        out = xp.full(tuple(shape), -xp.inf, dtype=a.dtype, device=xp_device(a))
        sgn = xp.sign(out)

    if xp.isdtype(out.dtype, 'complex floating'):
        if return_sign:
            real = xp.real(sgn)
            imag = xp_float_to_complex(_wrap_radians(xp.imag(sgn), xp=xp), xp=xp)
            sgn = real + imag*1j
        else:
            real = xp.real(out)
            imag = xp_float_to_complex(_wrap_radians(xp.imag(out), xp=xp), xp=xp)
            out = real + imag*1j

    # Deal with shape details - reducing dimensions and convert 0-D to scalar for NumPy
    out = xp.squeeze(out, axis=axis) if not keepdims else out
    sgn = xp.squeeze(sgn, axis=axis) if (sgn is not None and not keepdims) else sgn
    out = out[()] if out.ndim == 0 else out
    sgn = sgn[()] if (sgn is not None and sgn.ndim == 0) else sgn

    return (out, sgn) if return_sign else out


def logsumexp(a: ArrayLike, axis: Axis = None, b: ArrayLike | None = None,
              keepdims: bool = False, return_sign: Literal[False] = False, where: ArrayLike | None = None) -> Array: ...


def logsumexp(a: ArrayLike, axis: Axis = None, b: ArrayLike | None = None,
              keepdims: bool = False, *, return_sign: Literal[True], where: ArrayLike | None = None) -> tuple[Array, Array]: ...


def logsumexp(a: ArrayLike, axis: Axis = None, b: ArrayLike | None = None,
              keepdims: bool = False, return_sign: bool = False, where: ArrayLike | None = None) -> Array | tuple[Array, Array]: ...


def logsumexp(a: ArrayLike, axis: Axis = None, b: ArrayLike | None = None,
              keepdims: bool = False, return_sign: bool = False, where: ArrayLike | None = None) -> Array | tuple[Array, Array]:
  r"""Log-sum-exp reduction.

  JAX implementation of :func:`scipy.special.logsumexp`.

  .. math::
    \operatorname{logsumexp} a = \log \sum_i b_i \exp a_i

  where the :math:`i` indices range over one or more dimensions to be reduced.

  Args:
    a: the input array
    axis: int or sequence of ints, default=None. Axis along which the sum to be
      computed. If None, the sum is computed along all the axes.
    b: scaling factors for the exponentials. Must be broadcastable to the shape of `a`.
    keepdims: If ``True``, the axes that are reduced are left in the output as
      dimensions of size 1.
    return_sign: If ``True``, the output will be a ``(result, sign)`` pair,
      where ``sign`` is the sign of the sums and ``result`` contains the
      logarithms of their absolute values. If ``False`` only ``result`` is
      returned and it will contain NaN values if the sums are negative.
    where: Elements to include in the reduction.

  Returns:
    Either an array ``result`` or a pair of arrays ``(result, sign)``, depending
    on the value of the ``return_sign`` argument.

  See also:
    :func:`jax.nn.logmeanexp`
  """
  if where is not None:
    a = jnp.where(where, a, 0)
  if b is not None:
    a_arr, b_arr = promote_args_inexact("logsumexp", a, b)
    a_arr = jnp.where(b_arr != 0, a_arr, -np.inf)
  else:
    a_arr, = promote_args_inexact("logsumexp", a)
    b_arr = a_arr  # for type checking
  pos_dims, dims = _reduction_dims(a_arr, axis)
  amax = reductions.max(a_arr.real, axis=dims, keepdims=keepdims, where=where, initial=-np.inf)
  amax = lax.stop_gradient(lax.select(ufuncs.isfinite(amax), amax, lax.full_like(amax, 0)))
  amax_with_dims = amax if keepdims else lax.expand_dims(amax, pos_dims)

  exp_a = lax.exp(lax.sub(a_arr, amax_with_dims.astype(a_arr.dtype)))
  if b is not None:
    exp_a = lax.mul(exp_a, b_arr)
  sumexp = exp_a.sum(axis=dims, keepdims=keepdims, where=where)
  sign = lax.sign(sumexp)
  if return_sign or not np.issubdtype(a_arr.dtype, np.complexfloating):
    sumexp = abs(sumexp)
  out = lax.add(lax.log(sumexp), amax.astype(sumexp.dtype))

  if return_sign:
    return (out, sign)
  if b is not None and not np.issubdtype(out.dtype, np.complexfloating):
    with config.debug_nans(False):
      out = jnp.where(sign < 0, jnp.array(np.nan, dtype=out.dtype), out)
  return out

