from typing import Any

def projection_vector(x: Any, a: Any) -> Any:
  r"""Projection onto a vector.

  Projects a tree ``x`` onto the vector defined by a tree ``a``:

  .. math::

    \operatorname{proj}_a x = \frac{\langle x, a \rangle}{\langle a, a \rangle}
    a

  Args:
    x: tree to project.
    a: tree onto which to project. Must have the same structure as ``x``.

  Returns:
    tree with the same structure as ``x``.
  """
  scalar = optax.tree.vdot(x, a) / optax.tree.vdot(a, a)
  return optax.tree.scale(scalar, a)

