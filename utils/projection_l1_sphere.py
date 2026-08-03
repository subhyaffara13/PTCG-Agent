from typing import Any

def projection_l1_sphere(tree: Any, scale: jax.typing.ArrayLike = 1) -> Any:
  r"""Projection onto the l1 sphere.

  This function solves the following constrained optimization problem,
  where ``x`` is the input tree.

  .. math::

    \underset{y}{\text{argmin}} ~ \|x - y\|_2^2 \quad \textrm{subject to} \quad
    \|y\|_1 = \text{scale}

  Args:
    tree: tree to project.
    scale: radius of the sphere.

  Returns:
    projected tree, with the same structure as ``tree``.
  """
  tree_abs = jax.tree.map(jnp.abs, tree)
  tree_sign = jax.tree.map(jnp.sign, tree)
  tree_abs_proj = projection_simplex(tree_abs, scale)
  return optax.tree.mul(tree_sign, tree_abs_proj)

