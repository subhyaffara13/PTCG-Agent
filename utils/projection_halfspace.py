
def projection_halfspace(x: Any, a: Any, b: jax.typing.ArrayLike) -> Any:
  r"""Projection onto a halfspace.

  Projects a tree ``x`` onto the halfspace defined by a tree ``a`` and scalar
  ``b``.

  .. math::

    \operatorname{argmin}_y \|x - y\|_2^2 \quad \text{subject to} \quad
    \langle a, y \rangle \leq b

  Args:
    x: tree to project.
    a: tree defining halfspace onto which to project. Must have the same
      structure as ``x``.
    b: scalar defining halfspace onto which to project.

  Returns:
    tree with the same structure as ``x``.
  """
  scalar = (b - optax.tree.vdot(x, a)) / optax.tree.vdot(a, a)
  scalar = jnp.clip(scalar, max=0)
  return optax.tree.add_scale(x, scalar, a)

