from typing import Optional

def squared_error(
    predictions: jax.typing.ArrayLike,
    targets: Optional[jax.typing.ArrayLike] = None,
) -> jax.Array:
  """Calculates the squared error for a set of predictions.

  Mean Squared Error can be computed as squared_error(a, b).mean().

  Args:
    predictions: a vector of arbitrary shape `[...]`.
    targets: a vector with shape broadcastable to that of `predictions`; if not
      provided then it is assumed to be a vector of zeros.

  Returns:
    elementwise squared differences, with same shape as `predictions`.

  .. note::
    l2_loss = 0.5 * squared_error, where the 0.5 term is standard in
    "Pattern Recognition and Machine Learning" by Bishop, but not
    "The Elements of Statistical Learning" by Tibshirani.
  """
  utils.check_subdtype(predictions, jnp.floating)
  if targets is not None:
    # Avoid broadcasting logic for "-" operator.
    utils.check_shapes_equal(predictions, targets)
  errors = predictions - targets if targets is not None else predictions
  return errors**2  # pytype: disable=bad-return-type  # jax-arraylike

