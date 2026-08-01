
def expm1(a):
    return prims.expm1(a)


def expm1(ctx, x):
    if not x:
        return ctx.zero
    # exp(x) - 1 ~ x
    if ctx.mag(x) < -ctx.prec:
        return x + 0.5*x**2
    # TODO: accurately eval the smaller of the real/imag parts
    return ctx.sum_accurately(lambda: iter([ctx.exp(x),-1]),1)


def expm1(operand: _ods_ir.Value, *, fastmath: _Optional[_Union[_Any, _ods_ir.Attribute]] = None, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return ExpM1Op(operand=operand, fastmath=fastmath, results=results, loc=loc, ip=ip).result


def expm1(x: ArrayLike, *, accuracy: Tolerance | AccuracyMode | None = None) -> Array:
  r"""Elementwise :math:`e^{x} - 1`.

  This function lowers directly to the `stablehlo.exponential_minus_one`_
  operation. Compared to the naive expression ``lax.exp(x) - 1``, it is
  more accurate for ``x`` near zero.

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
    exponential minus 1.

  See also:
    - :func:`jax.lax.exp`: elementwise exponentional: :math:`e^x`.
    - :func:`jax.lax.log1p`: elementwise :math:`\mathrm{log}(1 + x)`.

  .. _stablehlo.exponential_minus_one: https://openxla.org/stablehlo/spec#exponential_minus_one
  """
  return expm1_p.bind(x, accuracy=accuracy)


def expm1(x: ArrayLike, /) -> Array:
  """Calculate ``exp(x)-1`` of each element of the input.

  JAX implementation of :obj:`numpy.expm1`.

  Args:
    x: input array or scalar.

  Returns:
    An array containing ``exp(x)-1`` of each element in ``x``, promotes to inexact
    dtype.

  Note:
    ``jnp.expm1`` has much higher precision than the naive computation of
    ``exp(x)-1`` for small values of ``x``.

  See also:
    - :func:`jax.numpy.log1p`: Calculates element-wise logarithm of one plus input.
    - :func:`jax.numpy.exp`: Calculates element-wise exponential of the input.
    - :func:`jax.numpy.exp2`: Calculates base-2 exponential of each element of
      the input.

  Examples:
    >>> x = jnp.array([2, -4, 3, -1])
    >>> with jnp.printoptions(precision=2, suppress=True):
    ...   print(jnp.expm1(x))
    [ 6.39 -0.98 19.09 -0.63]
    >>> with jnp.printoptions(precision=2, suppress=True):
    ...   print(jnp.exp(x)-1)
    [ 6.39 -0.98 19.09 -0.63]

    For values very close to 0, ``jnp.expm1(x)`` is much more accurate than
    ``jnp.exp(x)-1``:

    >>> x1 = jnp.array([1e-4, 1e-6, 2e-10])
    >>> jnp.expm1(x1)
    Array([1.0000500e-04, 1.0000005e-06, 2.0000000e-10], dtype=float32)
    >>> jnp.exp(x1)-1
    Array([1.00016594e-04, 9.53674316e-07, 0.00000000e+00], dtype=float32)
  """
  return lax.expm1(*promote_args_inexact('expm1', x))

