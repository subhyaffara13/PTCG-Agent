
def lt(val):
    """
    A validator that raises `ValueError` if the initializer is called with a
    number larger or equal to *val*.

    The validator uses `operator.lt` to compare the values.

    Args:
        val: Exclusive upper bound for values.

    .. versionadded:: 21.3.0
    """
    return _NumberValidator(val, "<", operator.lt)


def lt(a: TensorLikeType, b: TensorLikeType) -> TensorLikeType:
    return prims.lt(a, b)


def lt(left, right):
    """Compare sizes: only use on inputs known to be >= 0."""
    if V.graph.sizevars.guard_or_false(sympy.Lt(left, right)):
        return True

    # GCD fallback: if gcd(left, right) == left then left divides right,
    # so left <= right.  Combined with left != right this gives left < right.
    #
    # TODO: This is NOT always sound for unbacked symints.
    # e.g. lt(u0, 10*u0): gcd=u0, gcd==left, u0 != 10*u0 → returns True,
    # but if u0=0 then 0 < 0 is False.  The >= 0 checks mitigate the
    # negative case but the zero case remains.
    # TODO shall we add a runtime assertion at least.
    gcd = sympy.gcd(left, right)
    if gcd == left:
        return left != right

    return False


def lt(g: jit_utils.GraphContext, input, other):
    return _comparison_operator(g, input, other, "Less")


def lt(g: jit_utils.GraphContext, input, other):
    return _lt_impl(g, input, other)


def LT(f, *gens, **args):
    """
    Return the leading term of ``f``.

    Examples
    ========

    >>> from sympy import LT
    >>> from sympy.abc import x, y

    >>> LT(4*x**2 + 2*x*y**2 + x*y + 3*y)
    4*x**2

    """
    options.allowed_flags(args, ['polys'])

    try:
        F, opt = poly_from_expr(f, *gens, **args)
    except PolificationFailed as exc:
        raise ComputationFailed('LT', 1, exc)

    monom, coeff = F.LT(order=opt.order)
    return coeff*monom.as_expr()


def lt(n):
    """
    Match any value less than n
    """
    return between(None, n, inclusive_max=False)


def lt(x: ArrayLike, y: ArrayLike) -> Array:
  r"""Elementwise less-than: :math:`x < y`.

  This function lowers directly to the `stablehlo.compare`_ operation
  with ``comparison_direction=LT`` and ``compare_type`` set according
  to the input dtype.

  Args:
    x, y: Input arrays. Must have matching non-complex dtypes. If neither is
      a scalar, ``x`` and ``y`` must have the same number of dimensions and
      be broadcast compatible.

  Returns:
    A boolean array of shape ``lax.broadcast_shapes(x.shape, y.shape)``
    containing the elementwise less-than comparison.

  See also:
    - :func:`jax.numpy.less`: NumPy wrapper for this API, also accessible
      via the ``x < y`` operator on JAX arrays.
    - :func:`jax.lax.eq`: elementwise equal
    - :func:`jax.lax.ne`: elementwise not-equal
    - :func:`jax.lax.ge`: elementwise greater-than-or-equal
    - :func:`jax.lax.gt`: elementwise greater-than
    - :func:`jax.lax.le`: elementwise less-than-or-equal

  .. _stablehlo.compare: https://openxla.org/stablehlo/spec#compare
  """
  x, y = core.auto_insert_reshard(x, y)
  return lt_p.bind(x, y)


def lt(x: VectorClock, y: VectorClock) -> bool:
  return bool((x <= y).all() & (x < y).any())

