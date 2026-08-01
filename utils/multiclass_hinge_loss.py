
def multiclass_hinge_loss(
    scores: jax.typing.ArrayLike,
    labels: jax.typing.ArrayLike,
) -> jax.Array:
  """Multiclass hinge loss.

  Args:
    scores: scores produced by the model (floats).
    labels: ground-truth integer labels.

  Returns:
    loss values

  References:
    `Hinge loss <https://en.wikipedia.org/wiki/Hinge_loss>`_, Wikipedia

  .. versionadded:: 0.2.3
  """
  one_hot_labels = jax.nn.one_hot(labels, scores.shape[-1])  # pytype: disable=attribute-error  # jax-arraylike # noqa: E501
  return jnp.max(scores + 1.0 - one_hot_labels, axis=-1) - _dot_last_dim(
      scores, one_hot_labels
  )

