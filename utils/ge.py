
def ge(val):
    """
    A validator that raises `ValueError` if the initializer is called with a
    number smaller than *val*.

    The validator uses `operator.ge` to compare the values.

    Args:
        val: Inclusive lower bound for values

    .. versionadded:: 21.3.0
    """
    return _NumberValidator(val, ">=", operator.ge)


def ge(a: TensorLikeType, b: TensorLikeType) -> TensorLikeType:
    return prims.ge(a, b)


def ge(g: jit_utils.GraphContext, input, other):
    return g.op("GreaterOrEqual", input, other)


def ge(g: jit_utils.GraphContext, input, other):
    return _lt_impl(g, input, other)


def ge(n):
    """
    Match any value greater or equal to n
    """
    return between(n, None, inclusive_min=True)


def ge(x: ArrayLike, y: ArrayLike) -> Array:
  r"""Elementwise greater-than-or-equals: :math:`x \geq y`.

  This function lowers directly to the `stablehlo.compare`_ operation
  with ``comparison_direction=GE`` and ``compare_type`` set according
  to the input dtype.

  Args:
    x, y: Input arrays. Must have matching non-complex dtypes. If neither is
      a scalar, ``x`` and ``y`` must have the same number of dimensions and
      be broadcast compatible.

  Returns:
    A boolean array of shape ``lax.broadcast_shapes(x.shape, y.shape)``
    containing the elementwise greater-than-or-equal comparison.

  See also:
    - :func:`jax.numpy.greater_equal`: NumPy wrapper for this API, also
      accessible via the ``x >= y`` operator on JAX arrays.
    - :func:`jax.lax.eq`: elementwise equal
    - :func:`jax.lax.ne`: elementwise not-equal
    - :func:`jax.lax.gt`: elementwise greater-than
    - :func:`jax.lax.le`: elementwise less-than-or-equal
    - :func:`jax.lax.lt`: elementwise less-than

  .. _stablehlo.compare: https://openxla.org/stablehlo/spec#compare
  """
  x, y = core.auto_insert_reshard(x, y)
  return ge_p.bind(x, y)

