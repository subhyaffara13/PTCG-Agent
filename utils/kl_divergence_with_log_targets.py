from typing import Union

def kl_divergence_with_log_targets(
    log_predictions: jax.typing.ArrayLike,
    log_targets: jax.typing.ArrayLike,
    axis: Union[int, tuple[int, ...], None] = -1,
    where: Union[jax.typing.ArrayLike, None] = None,
) -> jax.Array:
  """Computes the Kullback-Leibler divergence (relative entropy) loss.

  Version of kl_div_loss where targets are given in log-space.

  Args:
    log_predictions: Probabilities of predicted distribution with shape [...,
      dim]. Expected to be in the log-space to avoid underflow.
    log_targets: Probabilities of target distribution with shape [..., dim].
      Expected to be in the log-space.
    axis: Axis or axes along which to compute.
    where: Elements to include in the computation.

  Returns:
    Kullback-Leibler divergence of predicted distribution from target
    distribution with shape [...].

  .. versionchanged:: 0.2.4
    Added ``axis`` and ``where`` arguments.
  """
  utils.check_subdtype(log_predictions, jnp.floating)
  utils.check_subdtype(log_targets, jnp.floating)
  loss = jnp.exp(log_targets) * (log_targets - log_predictions)
  return jnp.sum(loss, axis=axis, where=where)

