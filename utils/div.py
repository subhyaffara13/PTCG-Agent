
def div(a, b):
    a, b = promote_constants(
        (a, b), type_promotion_kind=ELEMENTWISE_TYPE_PROMOTION_KIND.INT_TO_FLOAT
    )
    return div_prim(a, b)


def div(
    a: TensorLikeType | NumberType,
    b: TensorLikeType | NumberType,
    *,
    rounding_mode: str | None = None,
):
    """
    Reference implementation of torch.div
    """
    if rounding_mode is None:
        return true_divide(a, b)
    elif rounding_mode == "trunc":
        return trunc_divide(a, b)
    elif rounding_mode == "floor":
        return floor_divide(a, b)
    else:
        msg = f"div expected rounding_mode to be one of None, 'trunc', or 'floor' but found {rounding_mode}."
        raise ValueError(msg)


def div(g: jit_utils.GraphContext, self, other, *args):
    if len(args) == 0:
        return opset9.true_divide(g, self, other)
    else:
        return _div_rounding_mode(g, self, other, *args)


def div(g: jit_utils.GraphContext, self, other, *args):
    if len(args) == 0:
        return true_divide(g, self, other)
    else:
        return _div_rounding_mode(g, self, other, *args)


def div(f, g, *gens, **args):
    """
    Compute polynomial division of ``f`` and ``g``.

    Examples
    ========

    >>> from sympy import div, ZZ, QQ
    >>> from sympy.abc import x

    >>> div(x**2 + 1, 2*x - 4, domain=ZZ)
    (0, x**2 + 1)
    >>> div(x**2 + 1, 2*x - 4, domain=QQ)
    (x/2 + 1, 5)

    """
    options.allowed_flags(args, ['auto', 'polys'])

    try:
        (F, G), opt = parallel_poly_from_expr((f, g), *gens, **args)
    except PolificationFailed as exc:
        raise ComputationFailed('div', 2, exc)

    q, r = F.div(G, auto=opt.auto)

    if not opt.polys:
        return q.as_expr(), r.as_expr()
    else:
        return q, r


def div(lhs, rhs):
  if dtypes.issubdtype(dtypes.result_type(lhs), np.integer):
    quotient = np.floor_divide(lhs, rhs)
    select = np.logical_and(np.sign(lhs) != np.sign(rhs),
                             np.remainder(lhs, rhs) != 0)
    return np.where(select, quotient + 1, quotient)
  else:
    return np.divide(lhs, rhs)


def div(x: ArrayLike, y: ArrayLike) -> Array:
  r"""Elementwise division: :math:`x \over y`.

  This function lowers directly to the `stablehlo.divide`_ operation.

  Integer division overflow (division by zero or signed division of
  INT_SMIN with -1) produces an implementation defined value.

  Args:
    x, y: Input arrays. Must have matching numerical dtypes. If neither
      is a scalar, ``x`` and ``y`` must have the same number of dimensions
      and be broadcast compatible.

  Returns:
    An array of the same dtype as ``x`` and ``y`` containing the quotient
    of each pair of broadcasted entries. For integer inputs, any fractional
    part is discarded.

  See also:
    - :func:`jax.numpy.divide`: NumPy-style true division supporting
      inputs with mixed dtypes and ranks.
    - :func:`jax.numpy.floor_divide`: NumPy-style floor division supporting
      inputs with mixed dtypes and ranks.

  .. _stablehlo.divide: https://openxla.org/stablehlo/spec#divide
  """
  x, y = core.auto_insert_reshard(x, y)
  return div_p.bind(x, y)

