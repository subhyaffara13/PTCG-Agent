from typing import Any

def projection_box(tree: Any, lower: Any, upper: Any) -> Any:
  r"""Projection onto box constraints.

  .. math::

    \underset{p}{\text{argmin}} ~ \|x - p\|_2^2 \quad \textrm{subject to} \quad
    \text{lower} \le p \le \text{upper}

  where :math:`x` is the input tree.

  Args:
    tree: tree to project.
    lower:  lower bound, a scalar or tree with the same structure as
      ``tree``.
    upper:  upper bound, a scalar or tree with the same structure as
      ``tree``.

  Returns:
    projected tree, with the same structure as ``tree``.
  """
  return jax.tree.map(jnp.clip, tree, lower, upper)

