
def scale_by_trust_ratio(
    min_norm: jax.typing.ArrayLike = 0.0,
    trust_coefficient: jax.typing.ArrayLike = 1.0,
    eps: jax.typing.ArrayLike = 0.0,
) -> base.GradientTransformation:
  """Scale updates by `trust ratio`.

  Used in :func:`optax.fromage`, :func:`optax.lars`, :func:`optax.lamb`.

  Args:
    min_norm: Minimum norm for params and gradient norms; by default is zero.
    trust_coefficient: A multiplier for the trust ratio.
    eps: Additive constant added to the denominator for numerical stability.

  Returns:
    A :class:`optax.GradientTransformation` object.
  """

  def update_fn(updates, state, params):
    if params is None:
      raise ValueError(base.NO_PARAMS_MSG)

    def _scale_update(update, param):

      # Clip norms to minimum value, by default no clipping.
      param_norm = numerics.safe_norm(param, min_norm)
      update_norm = numerics.safe_norm(update, min_norm)
      trust_ratio = trust_coefficient * param_norm / (update_norm + eps)

      # If no minimum norm clipping is used
      # Set trust_ratio to 1 in case where parameters would never be updated.
      zero_norm = jnp.logical_or(param_norm == 0.0, update_norm == 0.0)
      safe_trust_ratio = jnp.where(
          zero_norm, jnp.array(1.0, dtype=param.dtype), trust_ratio
      )

      return update * safe_trust_ratio

    updates = jax.tree.map(_scale_update, updates, params)
    return updates, state

  return base.GradientTransformation(base.init_empty_state, update_fn)

