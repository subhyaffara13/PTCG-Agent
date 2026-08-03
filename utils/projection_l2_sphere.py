from typing import Any

def projection_l2_sphere(tree: Any, scale: jax.typing.ArrayLike = 1) -> Any:
  r"""Projection onto the l2 sphere.

  This function solves the following constrained optimization problem,
  where ``x`` is the input tree.

  .. math::

    \underset{y}{\text{argmin}} ~ \|x - y\|_2^2 \quad \textrm{subject to} \quad
    \|y\|_2 = \text{value}

  Args:
    tree: tree to project.
    scale: radius of the sphere.

  Returns:
    projected tree, with the same structure as ``tree``.

  .. versionadded:: 0.2.4
  """
  factor = scale / optax.tree.norm(tree)
  return optax.tree.scale(factor, tree)

