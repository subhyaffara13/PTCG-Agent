
def gt(val):
    """
    A validator that raises `ValueError` if the initializer is called with a
    number smaller or equal to *val*.

    The validator uses `operator.gt` to compare the values.

    Args:
       val: Exclusive lower bound for values

    .. versionadded:: 21.3.0
    """
    return _NumberValidator(val, ">", operator.gt)


def gt(a: TensorLikeType, b: TensorLikeType) -> TensorLikeType:
    return prims.gt(a, b)


def gt(g: jit_utils.GraphContext, input, other):
    return _comparison_operator(g, input, other, "Greater")


def gt(g: jit_utils.GraphContext, input, other):
    return _gt_impl(g, input, other)


def gt(n):
    """
    Match any value greater than n
    """
    return between(n, None, inclusive_min=False)


def gt(x: ArrayLike, y: ArrayLike) -> Array:
  r"""Elementwise greater-than: :math:`x > y`.

  This function lowers directly to the `stablehlo.compare`_ operation
  with ``comparison_direction=GT`` and ``compare_type`` set according
  to the input dtype.

  Args:
    x, y: Input arrays. Must have matching non-complex dtypes. If neither is
      a scalar, ``x`` and ``y`` must have the same number of dimensions and
      be broadcast compatible.

  Returns:
    A boolean array of shape ``lax.broadcast_shapes(x.shape, y.shape)``
    containing the elementwise greater-than comparison.

  See also:
    - :func:`jax.numpy.greater`: NumPy wrapper for this API, also accessible
      via the ``x > y`` operator on JAX arrays.
    - :func:`jax.lax.eq`: elementwise equal
    - :func:`jax.lax.ne`: elementwise not-equal
    - :func:`jax.lax.ge`: elementwise greater-than-or-equal
    - :func:`jax.lax.le`: elementwise less-than-or-equal
    - :func:`jax.lax.lt`: elementwise less-than

  .. _stablehlo.compare: https://openxla.org/stablehlo/spec#compare
  """
  x, y = core.auto_insert_reshard(x, y)
  return gt_p.bind(x, y)

