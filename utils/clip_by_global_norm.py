
def clip_by_global_norm(
    max_norm: jax.typing.ArrayLike  # float
) -> base.GradientTransformation:
  """Clips updates using their global norm.

  Args:
    max_norm: The maximum global norm for an update.

  Returns:
    A :class:`optax.GradientTransformation` object.

  References:
    Pascanu et al., `On the difficulty of training Recurrent Neural Networks
    <https://arxiv.org/abs/1211.5063>`_, 2012
  """

  def update_fn(updates, state, params=None):
    del params
    g_norm = optax.tree.norm(updates)
    # TODO(b/163995078): revert back to the following (faster) implementation
    # once analyzed how it affects backprop through update (e.g. meta-gradients)
    # g_norm = jnp.maximum(max_norm, g_norm)
    # updates = jax.tree.map(lambda t: (t / g_norm) * max_norm, updates)
    trigger = jnp.squeeze(g_norm < max_norm)
    utils.check_rank(trigger, 0)  # A scalar.

    def clip_fn(t):
      return jax.lax.select(trigger, t, (t / g_norm.astype(t.dtype)) * max_norm)

    updates = jax.tree.map(clip_fn, updates)
    return updates, state

  return base.GradientTransformation(base.init_empty_state, update_fn)

