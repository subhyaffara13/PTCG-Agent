
def perceptron_loss(
    predictor_outputs: jax.typing.ArrayLike, targets: jax.typing.ArrayLike
) -> jax.Array:
  """Binary perceptron loss.

  Args:
    predictor_outputs: score produced by the model (float).
    targets: Target values. Target values should be strictly in the set {-1, 1}.

  Returns:
    loss value.

  References:
    `Perceptron <https://en.wikipedia.org/wiki/Perceptron>`_, Wikipedia
  """
  utils.check_shapes_equal(predictor_outputs, targets)
  return jnp.maximum(0, -predictor_outputs * targets)

