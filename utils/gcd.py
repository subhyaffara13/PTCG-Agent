
def gcd(a: TensorLikeType, b: TensorLikeType) -> TensorLikeType:
    return prims.gcd(a, b)


def gcd(f, g=None, *gens, **args):
    """
    Compute GCD of ``f`` and ``g``.

    Examples
    ========

    >>> from sympy import gcd
    >>> from sympy.abc import x

    >>> gcd(x**2 - 1, x**2 - 3*x + 2)
    x - 1

    """
    if hasattr(f, '__iter__'):
        if g is not None:
            gens = (g,) + gens

        return gcd_list(f, *gens, **args)
    elif g is None:
        raise TypeError("gcd() takes 2 arguments or a sequence of arguments")

    options.allowed_flags(args, ['polys'])

    try:
        (F, G), opt = parallel_poly_from_expr((f, g), *gens, **args)

        # gcd for domain Q[irrational] (purely algebraic irrational)
        a, b = map(sympify, (f, g))
        if a.is_algebraic and a.is_irrational and b.is_algebraic and b.is_irrational:
            frc = (a/b).ratsimp()
            if frc.is_rational:
                # abs ensures that the returned gcd is always non-negative
                return abs(a/frc.as_numer_denom()[0])

    except PolificationFailed as exc:
        domain, (a, b) = construct_domain(exc.exprs)

        try:
            return domain.to_sympy(domain.gcd(a, b))
        except NotImplementedError:
            raise ComputationFailed('gcd', 2, exc)

    result = F.gcd(G)

    if not opt.polys:
        return result.as_expr()
    else:
        return result


def gcd(*args):
    a = 0
    for b in args:
        if a:
            while b:
                a, b = b, a % b
        else:
            a = b
    return a


def gcd(x1: ArrayLike, x2: ArrayLike) -> Array:
  """Compute the greatest common divisor of two arrays.

  JAX implementation of :func:`numpy.gcd`.

  Args:
    x1: First input array. The elements must have integer dtype.
    x2: Second input array. The elements must have integer dtype.

  Returns:
    An array containing the greatest common divisors of the corresponding
    elements from the absolute values of `x1` and `x2`.

  See also:
    - :func:`jax.numpy.lcm`: compute the least common multiple of two arrays.

  Examples:
    Scalar inputs:

    >>> jnp.gcd(12, 18)
    Array(6, dtype=int32, weak_type=True)

    Array inputs:

    >>> x1 = jnp.array([12, 18, 24])
    >>> x2 = jnp.array([5, 10, 15])
    >>> jnp.gcd(x1, x2)
    Array([1, 2, 3], dtype=int32)

    Broadcasting:

    >>> x1 = jnp.array([12])
    >>> x2 = jnp.array([6, 9, 12])
    >>> jnp.gcd(x1, x2)
    Array([ 6,  3, 12], dtype=int32)
  """
  x1, x2 = util.ensure_arraylike("gcd", x1, x2)
  x1, x2 = util.promote_dtypes(x1, x2)
  if not issubdtype(x1.dtype, np.integer):
    raise ValueError("Arguments to jax.numpy.gcd must be integers.")
  x1, x2 = broadcast_arrays(x1, x2)
  gcd, _ = control_flow.while_loop(_gcd_cond_fn, _gcd_body_fn, (ufuncs.abs(x1), ufuncs.abs(x2)))
  return gcd

