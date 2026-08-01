
def tree_allclose(
    a: Any,
    b: Any,
    rtol: jax.typing.ArrayLike = 1e-05,
    atol: jax.typing.ArrayLike = 1e-08,
    equal_nan: bool = False
):
  """Check whether two trees are element-wise approximately equal within a tolerance.

  See :func:`jax.numpy.allclose` for the equivalent on arrays.

  Args:
    a: a tree
    b: a tree
    rtol: relative tolerance used for approximate equality
    atol: absolute tolerance used for approximate equality
    equal_nan: boolean indicating whether NaNs are treated as equal

  Returns:
    a boolean value.
  """  # noqa: E501
  def f(a, b):
    return jnp.allclose(a, b, rtol=rtol, atol=atol, equal_nan=equal_nan)
  tree = jax.tree.map(f, a, b)
  leaves = jax.tree.leaves(tree)
  result = functools.reduce(operator.and_, leaves, True)
  return result

