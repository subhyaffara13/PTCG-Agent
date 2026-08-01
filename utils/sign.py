
def sign(value: int) -> int:
    """Get sign of a numerical value.

    >>> sign(-5)
    -1
    >>> sign(10)
    1
    >>> sign(0)
    0

    :param value: The numerical value to get a sign from.
    :return: The sign of a numerical value.
    """
    if value > 0:
        return 1
    elif value < 0:
        return -1
    else:
        return 0


def sign(a):
    return prims.sign(a)


def sign(g: jit_utils.GraphContext, self):
    return g.op("Sign", self)


def Sign(f):
    return f[0]


def sign(e, x):
    """
    Returns a sign of an expression e(x) for x->oo.

    ::

        e >  0 for x sufficiently large ...  1
        e == 0 for x sufficiently large ...  0
        e <  0 for x sufficiently large ... -1

    The result of this function is currently undefined if e changes sign
    arbitrarily often for arbitrarily large x (e.g. sin(x)).

    Note that this returns zero only if e is *constantly* zero
    for x sufficiently large. [If e is constant, of course, this is just
    the same thing as the sign of e.]
    """
    if not isinstance(e, Basic):
        raise TypeError("e should be an instance of Basic")

    if e.is_positive:
        return 1
    elif e.is_negative:
        return -1
    elif e.is_zero:
        return 0

    elif not e.has(x):
        from sympy.simplify import logcombine
        e = logcombine(e)
        return _sign(e)
    elif e == x:
        return 1
    elif e.is_Mul:
        a, b = e.as_two_terms()
        sa = sign(a, x)
        if not sa:
            return 0
        return sa * sign(b, x)
    elif isinstance(e, exp):
        return 1
    elif e.is_Pow:
        if e.base == S.Exp1:
            return 1
        s = sign(e.base, x)
        if s == 1:
            return 1
        if e.exp.is_Integer:
            return s**e.exp
    elif isinstance(e, log) and e.args[0].is_positive:
        return sign(e.args[0] - 1, x)

    # if all else fails, do it the hard way
    c0, e0 = mrv_leadterm(e, x)
    return sign(c0, x)


def sign(x: Array, /, xp: Namespace, **kwargs: object) -> Array:
    if isdtype(x.dtype, "complex floating", xp=xp):
        out = (x / xp.abs(x, **kwargs))[...]
        # sign(0) = 0 but the above formula would give nan
        out[x == 0j] = 0j
    else:
        out = xp.sign(x, **kwargs)
    # CuPy sign() does not propagate nans. See
    # https://github.com/data-apis/array-api-compat/issues/136
    if is_cupy_namespace(xp) and isdtype(x.dtype, "real floating", xp=xp):
        out[xp.isnan(x)] = xp.nan
    return out[()]


def sign(x: Array, /) -> Array:
    # torch sign() does not support complex numbers and does not propagate
    # nans. See https://github.com/data-apis/array-api-compat/issues/136
    if x.dtype.is_complex:
        out = x/torch.abs(x)
        # sign(0) = 0 but the above formula would give nan
        out[x == 0+0j] = 0+0j
        return out
    else:
        out = torch.sign(x)
        if x.dtype.is_floating_point:
            out[torch.isnan(x)] = torch.nan
        return out


def sign(v):
    return -1 if v < 0 else (1 if v > 0 else 0)


def sign(ctx, x):
    x = ctx.convert(x)
    if not x or ctx.isnan(x):
        return x
    if ctx._is_real_type(x):
        if x > 0:
            return ctx.one
        else:
            return -ctx.one
    return x / abs(x)


def sign(operand: _ods_ir.Value[_ods_ir.RankedTensorType], *, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.RankedTensorType]:
  return SignOp(operand=operand, results=results, loc=loc, ip=ip).result


def sign(operand: _ods_ir.Value[_ods_ir.RankedTensorType], *, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.RankedTensorType]:
  return SignOp(operand=operand, results=results, loc=loc, ip=ip).result


def sign(x: ArrayLike) -> Array:
  r"""Elementwise sign.

  This function lowers directly to the `stablehlo.sign`_ operation.

  Args:
    x: input array

  Returns:
    Array of same shape and dtype as ``x``, containing the sign
    of the value, as defined in Notes below.

  Notes:
    For floating-point inputs, returns

    .. math::

       \mathrm{sign}(x) = \begin{cases}
         -1 & x < 0\\
         -0 & x = -0\\
         \mathit{NaN} & x = \mathit{NaN}\\
         +0 & x = +0\\
         1 & x > 0
      \end{cases}

    For signed integer inputs, returns

    .. math::

       \mathrm{sign}(x) = \begin{cases}
         -1 & x < 0\\
         0 & x = 0\\
         1 & x > 0
       \end{cases}

    For complex inputs, returns the complex phase, i.e.
    :math:`\mathrm{sign}(x) = x / |x|`.

  .. _stablehlo.sign: https://openxla.org/stablehlo/spec#sign
  """
  return sign_p.bind(x)


def sign(x: ArrayLike, /) -> Array:
  r"""Return an element-wise indication of sign of the input.

  JAX implementation of :obj:`numpy.sign`.

  The sign of ``x`` for real-valued input is:

  .. math::
    \mathrm{sign}(x) = \begin{cases}
      1, & x > 0\\
      0, & x = 0\\
      -1, & x < 0
    \end{cases}

  For complex valued input, ``jnp.sign`` returns a unit vector representing the
  phase. For generalized case, the sign of ``x`` is given by:

  .. math::
    \mathrm{sign}(x) = \begin{cases}
      \frac{x}{abs(x)}, & x \ne 0\\
      0, & x = 0
    \end{cases}

  Args:
    x: input array or scalar.

  Returns:
    An array with same shape and dtype as ``x`` containing the sign indication.

  See also:
    - :func:`jax.numpy.positive`: Returns element-wise positive values of the input.
    - :func:`jax.numpy.negative`: Returns element-wise negative values of the input.

  Examples:
    For Real-valued inputs:

    >>> x = jnp.array([0., -3., 7.])
    >>> jnp.sign(x)
    Array([ 0., -1.,  1.], dtype=float32)

    For complex-inputs:

    >>> x1 = jnp.array([1, 3+4j, 5j])
    >>> jnp.sign(x1)
    Array([1. +0.j , 0.6+0.8j, 0. +1.j ], dtype=complex64)
  """
  return lax.sign(*promote_args('sign', x))

