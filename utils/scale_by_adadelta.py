
def scale_by_adadelta(
    rho: jax.typing.ArrayLike = 0.9, eps: jax.typing.ArrayLike = 1e-6
) -> base.GradientTransformation:
  """Rescale updates according to the Adadelta algorithm.

  See :func:`optax.adadelta` for more details.

  Args:
    rho: A coefficient used for computing a running average of squared
      gradients.
    eps: Term added to the denominator to improve numerical stability.

  Returns:
    A :class:`optax.GradientTransformation` object.
  """

  def init_fn(params):
    e_g = optax.tree.zeros_like(params)  # E[squared gradient]
    e_x = optax.tree.zeros_like(params)  # E[squared update]
    return ScaleByAdaDeltaState(e_g=e_g, e_x=e_x)

  def update_fn(updates, state, params=None):
    del params
    e_g = optax.tree.update_moment(updates, state.e_g, rho, 2)
    updates = jax.tree.map(
        lambda g, cur_e_g, prev_e_x: (
            jnp.sqrt(prev_e_x + eps) / jnp.sqrt(cur_e_g + eps)
        )
        * g,
        updates,
        e_g,
        state.e_x,
    )
    e_x = optax.tree.update_moment(updates, state.e_x, rho, 2)
    return updates, ScaleByAdaDeltaState(e_g=e_g, e_x=e_x)

  return base.GradientTransformation(init_fn, update_fn)

