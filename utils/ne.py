
def ne(a: TensorLikeType, b: TensorLikeType) -> TensorLikeType:
    return prims.ne(a, b)


def ne(g: jit_utils.GraphContext, self, other):
    return eq(g, self, other)


def ne(x: ArrayLike, y: ArrayLike) -> Array:
  r"""Elementwise not-equals: :math:`x \neq y`.

  This function lowers directly to the `stablehlo.compare`_ operation
  with ``comparison_direction=NE`` and ``compare_type`` set according
  to the input dtype.

  Args:
    x, y: Input arrays. Must have matching dtypes. If neither is a
      scalar, ``x`` and ``y`` must have the same number of dimensions and
      be broadcast compatible.

  Returns:
    A boolean array of shape ``lax.broadcast_shapes(x.shape, y.shape)``
    containing the elementwise not-equal comparison.

  See also:
    - :func:`jax.numpy.not_equal`: NumPy wrapper for this API, also accessible
      via the ``x != y`` operator on JAX arrays.
    - :func:`jax.lax.eq`: elementwise equal
    - :func:`jax.lax.ge`: elementwise greater-than-or-equal
    - :func:`jax.lax.gt`: elementwise greater-than
    - :func:`jax.lax.le`: elementwise less-than-or-equal
    - :func:`jax.lax.lt`: elementwise less-than

  .. _stablehlo.compare: https://openxla.org/stablehlo/spec#compare
  """
  x, y = core.auto_insert_reshard(x, y)
  return ne_p.bind(x, y)

