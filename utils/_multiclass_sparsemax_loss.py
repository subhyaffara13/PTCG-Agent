
def _multiclass_sparsemax_loss(
    scores: jax.typing.ArrayLike, label: jax.typing.ArrayLike
) -> jax.Array:
  scores = jnp.asarray(scores)
  proba = projections.projection_simplex(scores)
  # Fenchel conjugate of the Gini negentropy, defined by:
  # cumulant = jnp.dot(proba, scores) + 0.5 * jnp.dot(proba, (1 - proba)).
  scores = (scores - scores[label]).at[label].set(0.0)
  return jnp.dot(proba, jnp.where(proba, scores, 0.0)) + 0.5 * (
      1.0 - jnp.dot(proba, proba)
  )

