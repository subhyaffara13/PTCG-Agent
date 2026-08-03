from typing import Any

def projection_l2_ball(tree: Any, scale: jax.typing.ArrayLike = 1) -> Any:
  r"""Projection onto the l2 ball.

  This function solves the following constrained optimization problem,
  where ``x`` is the input tree.

  .. math::

    \underset{y}{\text{argmin}} ~ \|x - y\|_2^2 \quad \textrm{subject to} \quad
    \|y\|_2 \le \text{scale}

  Args:
    tree: tree to project.
    scale: radius of the ball.

  Returns:
    projected tree, with the same structure as ``tree``.

  .. versionadded:: 0.2.4
  """
  squared_norm = optax.tree.norm(tree, squared=True)
  factor = scale / jnp.sqrt(jnp.maximum(squared_norm, scale**2))
  return optax.tree.scale(factor, tree)

