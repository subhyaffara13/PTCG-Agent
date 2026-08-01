
def smooth_labels(
    labels: jax.typing.ArrayLike,
    alpha: jax.typing.ArrayLike,
    *,
    axis: Union[int, tuple[int, ...], None] = -1,
    where: Union[jax.typing.ArrayLike, None] = None,
) -> jax.Array:
  """Apply label smoothing.

  Label smoothing is often used in combination with a cross-entropy loss.
  Smoothed labels favor small logit gaps, and it has been shown that this can
  provide better model calibration by preventing overconfident predictions.

  Args:
    labels: One hot labels to be smoothed.
    alpha: The smoothing factor.
    axis: Axis or axes along which to compute.
    where: Elements to include in the computation.

  Returns:
    a smoothed version of the one hot input labels.

  References:
    Muller et al, `When does label smoothing help?
    <https://arxiv.org/abs/1906.02629>`_, 2019
  """
  utils.check_subdtype(labels, jnp.floating)
  if where is None:
    num_categories = jnp.size(labels, axis)
  else:
    num_categories = jnp.sum(where, axis, keepdims=True)
  return (1.0 - alpha) * labels + alpha / num_categories  # pytype: disable=bad-return-type  # jax-arraylike # noqa: E501

