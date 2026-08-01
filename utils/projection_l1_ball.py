
def projection_l1_ball(tree: Any, scale: jax.typing.ArrayLike = 1) -> Any:
  r"""Projection onto the l1 ball.

  This function solves the following constrained optimization problem,
  where ``x`` is the input tree.

  .. math::

    \underset{y}{\text{argmin}} ~ \|x - y\|_2^2 \quad \textrm{subject to} \quad
    \|y\|_1 \le \text{scale}

  Args:
    tree: tree to project.
    scale: radius of the ball.

  Returns:
    projected tree, with the same structure as ``tree``.

  Example:

      >>> import jax.numpy as jnp
      >>> from optax import tree, projections
      >>> data = {"w": jnp.array([2.5, 3.2]), "b": 0.5}
      >>> print(tree.norm(data, ord=1))
      6.2
      >>> new_data = projections.projection_l1_ball(data)
      >>> print(tree.norm(new_data, ord=1))
      1.0000002

  .. versionadded:: 0.2.4
  """
  l1_norm = optax.tree.norm(tree, ord=1)
  return jax.lax.cond(
      l1_norm <= scale,
      lambda tree: tree,
      lambda tree: projection_l1_sphere(tree, scale),
      operand=tree,
  )

