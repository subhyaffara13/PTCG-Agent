
def projection_non_negative(tree: Any) -> Any:
  r"""Projection onto the non-negative orthant.

  .. math::

    \underset{p}{\text{argmin}} ~ \|x - p\|_2^2 \quad
    \textrm{subject to} \quad p \ge 0

  where :math:`x` is the input tree.

  Args:
    tree: tree to project.

  Returns:
    projected tree, with the same structure as ``tree``.
  """
  return jax.tree.map(jax.nn.relu, tree)

