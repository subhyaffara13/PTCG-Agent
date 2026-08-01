
def float_power(
    a: TensorLikeType | NumberType,
    b: TensorLikeType | NumberType,
) -> Tensor:
    if isinstance(a, Number) and isinstance(b, Number):
        raise ValueError(
            "Receive two Number inputs to an elementwise binary operation!"
        )

    # Handles type promotion
    dtype = utils.get_higher_dtype(a, b)
    if dtype is None:
        raise AssertionError("dtype should not be None after get_higher_dtype")
    if utils.is_complex_dtype(dtype):
        dtype = torch.complex128
    else:
        dtype = torch.float64

    # Float power has the following contiguous cast behavior to be
    # consistent with its C++ impl

    a = _maybe_convert_to_dtype(a, dtype)

    b = _maybe_convert_to_dtype(b, dtype)

    a, b = _maybe_broadcast(a, b)

    return pow(a, b)


def float_power(x: ArrayLike, y: ArrayLike, /) -> Array:
  """Calculate element-wise base ``x`` exponential of ``y``.

  JAX implementation of :obj:`numpy.float_power`.

  Args:
    x: scalar or array. Specifies the bases.
    y: scalar or array. Specifies the exponents. ``x`` and ``y`` should either
      have same shape or be broadcast compatible.

  Returns:
    An array containing the base ``x`` exponentials of ``y``, promoting to the
    inexact dtype.

  See also:
    - :func:`jax.numpy.exp`: Calculates element-wise exponential of the input.
    - :func:`jax.numpy.exp2`: Calculates base-2 exponential of each element of
      the input.

  Examples:
    Inputs with same shape:

    >>> x = jnp.array([3, 1, -5])
    >>> y = jnp.array([2, 4, -1])
    >>> jnp.float_power(x, y)
    Array([ 9. ,  1. , -0.2], dtype=float32)

    Inputs with broadcast compatibility:

    >>> x1 = jnp.array([[2, -4, 1],
    ...                 [-1, 2, 3]])
    >>> y1 = jnp.array([-2, 1, 4])
    >>> jnp.float_power(x1, y1)
    Array([[ 0.25, -4.  ,  1.  ],
           [ 1.  ,  2.  , 81.  ]], dtype=float32)

    ``jnp.float_power`` produces ``nan`` for negative values raised to a non-integer
    values.

    >>> jnp.float_power(-3, 1.7)
    Array(nan, dtype=float32, weak_type=True)
  """
  out = lax.pow(*promote_args_inexact("float_power", x, y))
  jnp_error._set_error_if_nan(out)
  return out

