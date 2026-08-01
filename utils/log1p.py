
def log1p(a):
    return prims.log1p(a)


def log1p(g: jit_utils.GraphContext, self):
    return log(g, add(g, symbolic_helper._if_scalar_type_as(torch.ones(1), self), self))


def log1p(ctx, x):
    if not x:
        return ctx.zero
    if ctx.mag(x) < -ctx.prec:
        return x - 0.5*x**2
    return ctx.log(ctx.fadd(1, x, prec=2*ctx.prec))


def log1p(operand: _ods_ir.Value, *, fastmath: _Optional[_Union[_Any, _ods_ir.Attribute]] = None, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return Log1pOp(operand=operand, fastmath=fastmath, results=results, loc=loc, ip=ip).result


def log1p(x: ArrayLike, *, accuracy: Tolerance | AccuracyMode | None = None) -> Array:
  r"""Elementwise :math:`\mathrm{log}(1 + x)`.

  This function lowers directly to the  `stablehlo.log_plus_one`_ operation.
  Compared to the naive expression ``lax.log(1 + x)``, it is more accurate
  for ``x`` near zero.

  Args:
    x: input array. Must have floating-point or complex type.
    accuracy: Optional `lax.Tolerance` or `lax.AccuracyMode` object that
      selects the implementation of the op based on the requested accuracy. If
      the implementation cannot satisfy the requested tolerance, the
      compiler will return an error. If mode is specified and there are no
      multiple implementations available, the default implementation will be
      used.

  Returns:
    Array of the same shape and dtype as ``x`` containing the element-wise
    natural logarithm of ``x + 1``.

  See also:
    - :func:`jax.lax.expm1`: elementwise :math:`e^x - 1`.
    - :func:`jax.lax.log`: elementwise natural logarithm :math:`\mathrm{log}(x)`.

  .. _stablehlo.log_plus_one: https://openxla.org/stablehlo/spec#log_plus_one
  """
  return log1p_p.bind(x, accuracy=accuracy)


def log1p(x: ArrayLike, /) -> Array:
  """Calculates element-wise logarithm of one plus input, ``log(x+1)``.

  JAX implementation of :obj:`numpy.log1p`.

  Args:
    x: input array or scalar.

  Returns:
    An array containing the logarithm of one plus of each element in ``x``,
    promotes to inexact dtype.

  Note:
    ``jnp.log1p`` is more accurate than when using the naive computation of
    ``log(x+1)`` for small values of ``x``.

  See also:
    - :func:`jax.numpy.expm1`: Calculates :math:`e^x-1` of each element of the
      input.
    - :func:`jax.numpy.log2`: Calculates base-2 logarithm of each element of input.
    - :func:`jax.numpy.log`: Calculates element-wise logarithm of the input.

  Examples:
    >>> x = jnp.array([2, 5, 9, 4])
    >>> jnp.allclose(jnp.log1p(x), jnp.log(x+1))
    Array(True, dtype=bool)

    For values very close to 0, ``jnp.log1p(x)`` is more accurate than
    ``jnp.log(x+1)``:

    >>> x1 = jnp.array([1e-4, 1e-6, 2e-10])
    >>> jnp.expm1(jnp.log1p(x1))  # doctest: +SKIP
    Array([1.00000005e-04, 9.99999997e-07, 2.00000003e-10], dtype=float32)
    >>> jnp.expm1(jnp.log(x1+1))  # doctest: +SKIP
    Array([1.000166e-04, 9.536743e-07, 0.000000e+00], dtype=float32)
  """
  out = lax.log1p(*promote_args_inexact('log1p', x))
  jnp_error._set_error_if_nan(out)
  return out

