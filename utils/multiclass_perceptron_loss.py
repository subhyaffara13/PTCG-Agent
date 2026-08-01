
def multiclass_perceptron_loss(
    scores: jax.typing.ArrayLike,
    labels: jax.typing.ArrayLike,
) -> jax.Array:
  """Multiclass perceptron loss.

  Args:
    scores: scores produced by the model.
    labels: ground-truth integer labels.

  Returns:
    loss values.

  References:
    Michael Collins. Discriminative training methods for Hidden Markov Models:
    Theory and experiments with perceptron algorithms. EMNLP 2002

  .. versionadded:: 0.2.2
  """
  one_hot_labels = jax.nn.one_hot(labels, scores.shape[-1])  # pytype: disable=attribute-error  # jax-arraylike # noqa: E501
  return jnp.max(scores, axis=-1) - _dot_last_dim(scores, one_hot_labels)

