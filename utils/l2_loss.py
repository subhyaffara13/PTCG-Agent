
def l2_loss(
    predictions: jax.typing.ArrayLike,
    targets: Optional[jax.typing.ArrayLike] = None,
) -> jax.Array:
  """Calculates the L2 loss for a set of predictions.

  Args:
    predictions: a vector of arbitrary shape `[...]`.
    targets: a vector with shape broadcastable to that of `predictions`; if not
      provided then it is assumed to be a vector of zeros.

  Returns:
    elementwise squared differences, with same shape as `predictions`.

  .. note::
    the 0.5 term is standard in "Pattern Recognition and Machine Learning"
    by Bishop, but not "The Elements of Statistical Learning" by Tibshirani.
  """
  predictions = jnp.asarray(predictions)
  return 0.5 * squared_error(predictions, targets)

