
def convex_kl_divergence(
    log_predictions: jax.typing.ArrayLike,
    targets: jax.typing.ArrayLike,
    axis: Union[int, tuple[int, ...], None] = -1,
    where: Union[jax.typing.ArrayLike, None] = None,
) -> jax.Array:
  return generalized_kl_divergence(
      log_predictions, targets, axis=axis, where=where
  )

