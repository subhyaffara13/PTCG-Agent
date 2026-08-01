
def le(val):
    """
    A validator that raises `ValueError` if the initializer is called with a
    number greater than *val*.

    The validator uses `operator.le` to compare the values.

    Args:
        val: Inclusive upper bound for values.

    .. versionadded:: 21.3.0
    """
    return _NumberValidator(val, "<=", operator.le)


def le(a: TensorLikeType, b: TensorLikeType) -> TensorLikeType:
    return prims.le(a, b)


def le(g: jit_utils.GraphContext, input, other):
    return g.op("LessOrEqual", input, other)


def le(g: jit_utils.GraphContext, input, other):
    return _gt_impl(g, input, other)


def le(n):
    """
    Match any value less or equal to n
    """
    return between(None, n, inclusive_max=True)


def le(x: ArrayLike, y: ArrayLike) -> Array:
  r"""Elementwise less-than-or-equals: :math:`x \leq y`.

  This function lowers directly to the `stablehlo.compare`_ operation
  with ``comparison_direction=LE`` and ``compare_type`` set according
  to the input dtype.

  Args:
    x, y: Input arrays. Must have matching non-complex dtypes. If neither is
      a scalar, ``x`` and ``y`` must have the same number of dimensions and
      be broadcast compatible.

  Returns:
    A boolean array of shape ``lax.broadcast_shapes(x.shape, y.shape)``
    containing the elementwise less-than-or-equal comparison.

  See also:
    - :func:`jax.numpy.less_equal`: NumPy wrapper for this API, also
      accessible via the ``x <= y`` operator on JAX arrays.
    - :func:`jax.lax.eq`: elementwise equal
    - :func:`jax.lax.ne`: elementwise not-equal
    - :func:`jax.lax.ge`: elementwise greater-than-or-equal
    - :func:`jax.lax.gt`: elementwise greater-than
    - :func:`jax.lax.lt`: elementwise less-than

  .. _stablehlo.compare: https://openxla.org/stablehlo/spec#compare
  """
  x, y = core.auto_insert_reshard(x, y)
  return le_p.bind(x, y)

