
def rem(f, g, *gens, **args):
    """
    Compute polynomial remainder of ``f`` and ``g``.

    Examples
    ========

    >>> from sympy import rem, ZZ, QQ
    >>> from sympy.abc import x

    >>> rem(x**2 + 1, 2*x - 4, domain=ZZ)
    x**2 + 1
    >>> rem(x**2 + 1, 2*x - 4, domain=QQ)
    5

    """
    options.allowed_flags(args, ['auto', 'polys'])

    try:
        (F, G), opt = parallel_poly_from_expr((f, g), *gens, **args)
    except PolificationFailed as exc:
        raise ComputationFailed('rem', 2, exc)

    r = F.rem(G, auto=opt.auto)

    if not opt.polys:
        return r.as_expr()
    else:
        return r


def rem(lhs, rhs):
  return np.sign(lhs) * np.remainder(np.abs(lhs), np.abs(rhs))


def rem(x: ArrayLike, y: ArrayLike) -> Array:
  r"""Elementwise remainder: :math:`x \bmod y`.

  This function lowers directly to the `stablehlo.remainder`_ operation.
  The sign of the result is taken from the dividend, and the absolute value
  of the result is always less than the divisor's absolute value.

  Integer division overflow (remainder by zero or remainder of INT_SMIN with -1)
  produces an implementation defined value.

  Args:
    x, y: Input arrays. Must have matching int or float dtypes. If neither
      is a scalar, ``x`` and ``y`` must have the same number of dimensions
      and be broadcast compatible.

  Returns:
    An array of the same dtype as ``x`` and ``y`` containing the remainder.

  See also:
    - :func:`jax.numpy.remainder`: NumPy-style remainder with different
      sign semantics.

  .. _stablehlo.remainder: https://openxla.org/stablehlo/spec#remainder
  """
  x, y = core.auto_insert_reshard(x, y)
  return rem_p.bind(x, y)

