
def projection_hyperplane(x: Any, a: Any, b: jax.typing.ArrayLike) -> Any:
  r"""Projection onto a hyperplane.

  Projects a tree ``x`` onto the hyperplane defined by a tree ``a`` and scalar
  ``b``.

  .. math::

    \operatorname{argmin}_y \|x - y\|_2^2 \quad \text{subject to} \quad
    \langle a, y \rangle = b

  Args:
    x: tree to project.
    a: tree defining hyperplane onto which to project. Must have the same
      structure as ``x``.
    b: scalar defining hyperplane onto which to project.

  Returns:
    tree with the same structure as ``x``.
  """
  scalar = (b - optax.tree.vdot(x, a)) / optax.tree.vdot(a, a)
  return optax.tree.add_scale(x, scalar, a)

