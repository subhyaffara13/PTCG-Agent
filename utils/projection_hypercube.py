
def projection_hypercube(tree: Any, scale: Any = 1) -> Any:
  r"""Projection onto the (unit) hypercube.

  .. math::

    \underset{p}{\text{argmin}} ~ \|x - p\|_2^2 \quad \textrm{subject to} \quad
    0 \le p \le \text{scale}

  where :math:`x` is the input tree.

  By default, we project to the unit hypercube (`scale=1`).

  This is a convenience wrapper around
  :func:`projection_box <optax.projections.projection_box>`.

  Args:
    tree: tree to project.
    scale: scale of the hypercube, a scalar or a tree (default: 1).

  Returns:
    projected tree, with the same structure as ``tree``.
  """
  return projection_box(tree, lower=0, upper=scale)

