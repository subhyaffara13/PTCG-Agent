
def cosine_distance(
    predictions: jax.typing.ArrayLike,
    targets: jax.typing.ArrayLike,
    *,
    epsilon: jax.typing.ArrayLike = 0.0,
    axis: Union[int, tuple[int, ...], None] = -1,
    where: Union[jax.typing.ArrayLike, None] = None,
) -> jax.Array:
  r"""Computes the cosine distance between targets and predictions.

  The cosine **distance**, implemented here, measures the **dissimilarity**
  of two vectors as the opposite of cosine **similarity**: `1 - cos(\theta)`.

  Args:
    predictions: The predicted vectors, with shape `[..., dim]`.
    targets: Ground truth target vectors, with shape `[..., dim]`.
    epsilon: minimum norm for terms in the denominator of the cosine similarity.
    axis: Axis or axes along which to compute.
    where: Elements to include in the computation.

  Returns:
    cosine distances, with shape `[...]`.

  References:
    `Cosine distance
    <https://en.wikipedia.org/wiki/Cosine_similarity#Cosine_distance>`_,
    Wikipedia.

  .. versionchanged:: 0.2.4
    Added ``axis`` and ``where`` arguments.
  """
  utils.check_subdtype(predictions, jnp.floating)
  utils.check_subdtype(targets, jnp.floating)
  # cosine distance = 1 - cosine similarity.
  return 1.0 - cosine_similarity(
      predictions, targets, epsilon=epsilon, axis=axis, where=where
  )

