
def fmod(a, b):
    is_integral = is_boolean_type(a) or is_integer_type(a)

    if is_integral:

        def fn(a, b):
            return ops.mod(a, b)

    else:

        def fn(a, b):
            return ops.fmod(a, b)

    return make_pointwise(fn)(a, b)


def fmod(a: TensorLikeType, b: TensorLikeType) -> TensorLikeType:
    return prims.fmod(a, b)


def fmod(g: jit_utils.GraphContext, input, other):
    return g.op("Mod", input, other, fmod_i=1)


def fmod(ctx, x, y):
    return ctx.convert(x) % ctx.convert(y)


def fmod(x1: ArrayLike, x2: ArrayLike, /) -> Array:
  """Calculate element-wise floating-point modulo operation.

  JAX implementation of :obj:`numpy.fmod`.

  Args:
    x1: scalar or array. Specifies the dividend.
    x2: scalar or array. Specifies the divisor. ``x1`` and ``x2`` should either
       have same shape or be broadcast compatible.

  Returns:
    An array containing the result of the element-wise floating-point modulo
    operation of ``x1`` and ``x2`` with same sign as the elements of ``x1``.

  Note:
    The result of ``jnp.fmod`` is equivalent to ``x1 - x2 * jnp.trunc(x1 / x2)``.

  See also:
    - :func:`jax.numpy.mod` and :func:`jax.numpy.remainder`: Returns the element-wise
      remainder of the division.
    - :func:`jax.numpy.divmod`: Calculates the integer quotient and remainder of
      ``x1`` by ``x2``, element-wise.

  Examples:
    >>> x1 = jnp.array([[3, -1, 4],
    ...                 [8, 5, -2]])
    >>> x2 = jnp.array([2, 3, -5])
    >>> jnp.fmod(x1, x2)
    Array([[ 1, -1,  4],
           [ 0,  2, -2]], dtype=int32)
    >>> x1 - x2 * jnp.trunc(x1 / x2)
    Array([[ 1., -1.,  4.],
           [ 0.,  2., -2.]], dtype=float32)
  """
  x1, x2 = ensure_arraylike("fmod", x1, x2)
  if dtypes.issubdtype(dtypes.result_type(x1, x2), np.integer):
    x2 = _where(x2 == 0, lax._ones(x2), x2)
  out = lax.rem(*promote_args_numeric("fmod", x1, x2))
  jnp_error._set_error_if_nan(out)
  return out

