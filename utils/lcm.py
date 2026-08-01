
def lcm(a: TensorLikeType, b: TensorLikeType):
    dtype = a.dtype
    # promoting to int32 to maintain 100% consistency with C++ and to
    # prevent overflow in case of int8 and int16
    promote_to_int = dtype in (torch.int8, torch.int16)
    if promote_to_int:
        a = prims.convert_element_type(a, torch.int32)
        b = prims.convert_element_type(b, torch.int32)

    g = torch.gcd(a, b)
    # Avoid division by zero in case gcd(0, 0) == 0
    g = torch.where(g == 0, 1, g)
    res = torch.abs(prims.div(a, g) * b)
    return res if not promote_to_int else prims.convert_element_type(res, dtype)


def lcm(f, g=None, *gens, **args):
    """
    Compute LCM of ``f`` and ``g``.

    Examples
    ========

    >>> from sympy import lcm
    >>> from sympy.abc import x

    >>> lcm(x**2 - 1, x**2 - 3*x + 2)
    x**3 - 2*x**2 - x + 2

    """
    if hasattr(f, '__iter__'):
        if g is not None:
            gens = (g,) + gens

        return lcm_list(f, *gens, **args)
    elif g is None:
        raise TypeError("lcm() takes 2 arguments or a sequence of arguments")

    options.allowed_flags(args, ['polys'])

    try:
        (F, G), opt = parallel_poly_from_expr((f, g), *gens, **args)

        # lcm for domain Q[irrational] (purely algebraic irrational)
        a, b = map(sympify, (f, g))
        if a.is_algebraic and a.is_irrational and b.is_algebraic and b.is_irrational:
            frc = (a/b).ratsimp()
            if frc.is_rational:
                return a*frc.as_numer_denom()[1]

    except PolificationFailed as exc:
        domain, (a, b) = construct_domain(exc.exprs)

        try:
            return domain.to_sympy(domain.lcm(a, b))
        except NotImplementedError:
            raise ComputationFailed('lcm', 2, exc)

    result = F.lcm(G)

    if not opt.polys:
        return result.as_expr()
    else:
        return result


def lcm(x1: ArrayLike, x2: ArrayLike) -> Array:
  """Compute the least common multiple of two arrays.

  JAX implementation of :func:`numpy.lcm`.

  Args:
    x1: First input array. The elements must have integer dtype.
    x2: Second input array. The elements must have integer dtype.

  Returns:
    An array containing the least common multiple of the corresponding
    elements from the absolute values of `x1` and `x2`.

  See also:
    - :func:`jax.numpy.gcd`: compute the greatest common divisor of two arrays.

  Examples:
    Scalar inputs:

    >>> jnp.lcm(12, 18)
    Array(36, dtype=int32, weak_type=True)

    Array inputs:

    >>> x1 = jnp.array([12, 18, 24])
    >>> x2 = jnp.array([5, 10, 15])
    >>> jnp.lcm(x1, x2)
    Array([ 60,  90, 120], dtype=int32)

    Broadcasting:

    >>> x1 = jnp.array([12])
    >>> x2 = jnp.array([6, 9, 12])
    >>> jnp.lcm(x1, x2)
    Array([12, 36, 12], dtype=int32)
  """
  x1, x2 = util.ensure_arraylike("lcm", x1, x2)
  x1, x2 = util.promote_dtypes(x1, x2)
  x1, x2 = ufuncs.abs(x1), ufuncs.abs(x2)
  if not issubdtype(x1.dtype, np.integer):
    raise ValueError("Arguments to jax.numpy.lcm must be integers.")
  d = gcd(x1, x2)
  return where(d == 0, lax._const(d, 0),
               ufuncs.multiply(x1, ufuncs.floor_divide(x2, d)))

