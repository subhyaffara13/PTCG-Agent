from typing import Any

def projection_linf_ball(tree: Any, scale: jax.typing.ArrayLike = 1) -> Any:
  r"""Projection onto the l-infinity ball.

  This function solves the following constrained optimization problem,
  where ``x`` is the input tree.

  .. math::

    \underset{y}{\text{argmin}} ~ \|x - y\|_2^2 \quad \textrm{subject to} \quad
    \|y\|_{\infty} \le \text{scale}

  Args:
    tree: tree to project.
    scale: radius of the ball.

  Returns:
    projected tree, with the same structure as ``tree``.
  """
  lower = optax.tree.full_like(tree, -scale)
  upper = optax.tree.full_like(tree, scale)
  return projection_box(tree, lower=lower, upper=upper)

