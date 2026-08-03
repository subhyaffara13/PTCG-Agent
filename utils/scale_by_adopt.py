from typing import Callable, Optional

def scale_by_adopt(
    b1: jax.typing.ArrayLike = 0.9,
    b2: jax.typing.ArrayLike = 0.9999,
    eps: jax.typing.ArrayLike = 1e-6,
    mu_dtype: Optional[jax.typing.DTypeLike] = None,
    *,
    nesterov: bool = False,
    use_clipping: bool = True,
    clip_value_fn: Callable[[jax.Array], jax.Array] = lambda x: x**0.25,
) -> base.GradientTransformation:
  r"""Rescale updates according to the ADOPT algorithm.

  Args:
    b1: Decay rate for the exponentially weighted average of grads.
    b2: Decay rate for the exponentially weighted average of squared grads.
    eps: Term added to the denominator to improve numerical stability.
    mu_dtype: Optional `dtype` to be used for the first order accumulator; if
      `None` then the `dtype` is inferred from `params` and `updates`.
    nesterov: Whether to use Nesterov momentum.
    use_clipping: Whether to use gradient clipping to improve stability. When
      enabled, the clipping value is determined by the clip_value_fn.
    clip_value_fn: A function that takes a step index and returns a clipping
      value. Default is :math:`x^{0.25}`.

  Returns:
    A :class:`optax.GradientTransformation` object.

  .. seealso:: :func:`optax.contrib.adopt`
  """

  mu_dtype = utils.canonicalize_dtype(mu_dtype)

  def init_fn(params):
    mu = optax.tree.zeros_like(params, dtype=mu_dtype)  # First moment
    nu = optax.tree.zeros_like(params)  # Second moment
    return transform.ScaleByAdamState(
        count=jnp.zeros([], jnp.int32), mu=mu, nu=nu
    )

  def update_fn(updates, state, params=None):
    del params
    b2_ = jnp.where(state.count > 0, b2, 0)
    b1_ = jnp.where(state.count > 0, b1, 1)
    nu = optax.tree.update_moment_per_elem_norm(updates, state.nu, b2_, 2)
    if use_clipping:
      clip_value = clip_value_fn(state.count)
      mu_updates = jax.tree.map(
          lambda ud, nu: jnp.clip(
              ud / jnp.maximum(jnp.sqrt(nu), eps), -clip_value, clip_value
          ),
          updates,
          state.nu,
      )
    else:
      mu_updates = jax.tree.map(
          lambda ud, nu: ud / jnp.maximum(jnp.sqrt(nu), eps), updates, state.nu
      )
    mu = optax.tree.update_moment(mu_updates, state.mu, b1_, 1)
    count_inc = numerics.safe_increment(state.count)
    if nesterov:
      mu_ = optax.tree.update_moment(mu_updates, mu, b1_, 1)
    else:
      mu_ = mu
    updates = mu_
    mu = optax.tree.cast(mu, mu_dtype)
    return updates, transform.ScaleByAdamState(count=count_inc, mu=mu, nu=nu)

  return base.GradientTransformation(init_fn, update_fn)

