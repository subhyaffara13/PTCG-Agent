
def divmod(dividend: int, divisor: int) -> tuple[int, int]:
    """Divide the amount and get its quotient and remainder.

    >>> divmod(11, 3)
    (3, 2)
    >>> divmod(11.0, 3)  # doctest: +ELLIPSIS
    (3.666666666666666..., 0.0)

    :param dividend: The pot amount.
    :param divisor: The number of players.
    :return: The quotient and the remainder.
    """
    if isinstance(dividend, Integral):
        return builtins.divmod(dividend, divisor)

    quotient = dividend / divisor
    remainder = dividend - quotient * divisor

    return cast(tuple[int, int], (quotient, remainder))


def divmod(x, y):
    return x // y, x % y


def divmod(
    x1: ArrayLike,
    x2: ArrayLike,
    out1: OutArray | None = None,
    out2: OutArray | None = None,
    /,
    out: tuple[OutArray | None, OutArray | None] = (None, None),
    *,
    where: NotImplementedType = True,
    casting: CastingModes | None = "same_kind",
    order: NotImplementedType = "K",
    dtype: DTypeLike | None = None,
    subok: NotImplementedType = False,
    signature: NotImplementedType = None,
    extobj: NotImplementedType = None,
):
    # make sure we either have no out arrays at all, or there is either
    # out1, out2, or out=tuple, but not both
    num_outs = sum(x is not None for x in [out1, out2])
    if num_outs == 1:
        raise ValueError("both out1 and out2 need to be provided")
    elif num_outs == 2:
        o1, o2 = out
        if o1 is not None or o2 is not None:
            raise TypeError(
                "cannot specify 'out' as both a positional and keyword argument"
            )
    else:
        out1, out2 = out

    if dtype is None:
        dtype = _dtypes_impl.result_type_impl(x1, x2)
    x1, x2 = _util.typecast_tensors((x1, x2), dtype, casting)

    quot, rem = _binary_ufuncs_impl.divmod(x1, x2)

    quot = _ufunc_postprocess(quot, out1, casting)
    rem = _ufunc_postprocess(rem, out2, casting)
    return quot, rem


def divmod(x1: ArrayLike, x2: ArrayLike, /) -> tuple[Array, Array]:
  """Calculates the integer quotient and remainder of x1 by x2 element-wise

  JAX implementation of :obj:`numpy.divmod`.

  Args:
    x1: Input array, the dividend
    x2: Input array, the divisor

  Returns:
    A tuple of arrays ``(x1 // x2, x1 % x2)``.

  See Also:
    - :func:`jax.numpy.floor_divide`: floor division function
    - :func:`jax.numpy.remainder`: remainder function

  Examples:
    >>> x1 = jnp.array([10, 20, 30])
    >>> x2 = jnp.array([3, 4, 7])
    >>> jnp.divmod(x1, x2)
    (Array([3, 5, 4], dtype=int32), Array([1, 0, 2], dtype=int32))

    >>> x1 = jnp.array([-5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5])
    >>> x2 = 3
    >>> jnp.divmod(x1, x2)
    (Array([-2, -2, -1, -1, -1,  0,  0,  0,  1,  1,  1], dtype=int32),
     Array([1, 2, 0, 1, 2, 0, 1, 2, 0, 1, 2], dtype=int32))

    >>> x1 = jnp.array([6, 6, 6], dtype=jnp.int32)
    >>> x2 = jnp.array([1.9, 2.5, 3.1], dtype=jnp.float32)
    >>> jnp.divmod(x1, x2)
    (Array([3., 2., 1.], dtype=float32),
     Array([0.30000007, 1.        , 2.9       ], dtype=float32))
  """
  x1, x2 = promote_args_numeric("divmod", x1, x2)
  if dtypes.issubdtype(x1.dtype, np.integer):
    return floor_divide(x1, x2), remainder(x1, x2)
  else:
    jnp_error._set_error_if_divide_by_zero(x2)
    return _float_divmod(x1, x2)

