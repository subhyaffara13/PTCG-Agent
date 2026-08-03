from typing import Optional

def normalize_by_update_norm(
    scale_factor: jax.typing.ArrayLike = 1.0, eps: jax.typing.ArrayLike = 1e-6
) -> base.GradientTransformation:
  """Scale by the inverse of the update norm.

  Examples:
    >>> import optax
    >>> import jax
    >>> import jax.numpy as jnp
    >>> def f(x): return jnp.sum(x ** 2)  # simple quadratic function
    >>> solver = optax.normalize_by_update_norm(scale_factor=-1.0)
    >>> params = jnp.array([1., 2., 3.])
    >>> print('Objective function:', f(params))
    Objective function: 14.0
    >>> opt_state = solver.init(params)
    >>> for _ in range(5):
    ...  grad = jax.grad(f)(params)
    ...  updates, opt_state = solver.update(grad, opt_state, params)
    ...  params = optax.apply_updates(params, updates)
    ...  print('Objective function: {:.2E}'.format(f(params)))
    Objective function: 7.52E+00
    Objective function: 3.03E+00
    Objective function: 5.50E-01
    Objective function: 6.67E-02
    Objective function: 5.50E-01

  Args:
    scale_factor: factor by which the update will be multiplied (defaults to 1).
    eps: jitter term to avoid dividing by 0

  Returns:
    A :class:`optax.GradientTransformation` object.
  """

  def update_fn(
      updates: base.Updates,
      state: base.EmptyState,
      params: Optional[base.Params] = None,
  ) -> tuple[base.Updates, base.EmptyState]:
    del params
    g_norm = (optax.tree.norm(updates) + eps) / scale_factor
    updates = jax.tree.map(lambda g: g / g_norm, updates)
    return updates, state

  return base.GradientTransformation(base.init_empty_state, update_fn)

