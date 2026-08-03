from typing import Any

def projection_simplex(tree: Any, scale: jax.typing.ArrayLike = 1) -> Any:
  r"""Projection onto a simplex.

  This function solves the following constrained optimization problem,
  where ``x`` is the input tree.

  .. math::

    \underset{p}{\text{argmin}} ~ \|x - p\|_2^2 \quad \textrm{subject to} \quad
    p \ge 0, p^\top 1 = \text{scale}

  By default, the projection is onto the probability simplex (unit simplex).

  Args:
    tree: tree to project.
    scale: value the projected tree should sum to (default: 1).

  Returns:
    projected tree, a tree with the same structure as ``tree``.

  Example:

    Here is an example using a tree::

      >>> import jax.numpy as jnp
      >>> from optax import tree, projections
      >>> data = {"w": jnp.array([2.5, 3.2]), "b": 0.5}
      >>> print(tree.sum(data))
      6.2
      >>> new_data = projections.projection_simplex(data)
      >>> print(tree.sum(new_data))
      1.0000002

  .. versionadded:: 0.2.3
  """
  values, unravel_fn = flatten_util.ravel_pytree(tree)
  new_values = scale * _projection_unit_simplex(values / scale)
  return unravel_fn(new_values)

