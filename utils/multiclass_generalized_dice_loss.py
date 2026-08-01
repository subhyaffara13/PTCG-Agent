
def multiclass_generalized_dice_loss(
    predictions: jax.typing.ArrayLike,
    targets: jax.typing.ArrayLike,
    *,
    smooth: jax.typing.ArrayLike = 1.,
    apply_softmax: bool = True,
    ignore_background: bool = False,
) -> jax.Array:
  """Computes Multiclass Generalized Dice Loss with automatic class weighting.

  Computes Generalized Dice Loss where class weights are automatically
  computed as the inverse of the squared class frequencies. This helps
  handle class imbalance in segmentation tasks.

  Args:
      predictions: Logits of shape [..., num_classes].
      targets: One-hot encoded targets of shape [..., num_classes].
      smooth: Smoothing parameter.
      apply_softmax: Whether to apply softmax to predictions.
      ignore_background: If True, excludes the first class (index 0) from loss
            computation. Useful when class 0 represents background.

  Returns:
      Scalar loss value averaged across all classes and batch.

  References:
      Sudre et al. "Generalised Dice overlap as a deep learning loss function
      for highly unbalanced segmentations" (2017).
  """
  utils.check_shapes_equal(predictions, targets)

  # Compute class frequencies for weighting
  class_frequencies = jnp.sum(targets, axis=tuple(range(targets.ndim - 1)))  # pytype: disable=attribute-error  # jax-arraylike # noqa: E501

  # Compute weights as inverse of squared frequencies
  # Add small epsilon to avoid division by zero
  epsilon = 1e-7
  class_weights = 1.0 / (class_frequencies**2 + epsilon)

  # Normalize weights
  class_weights = class_weights / jnp.sum(class_weights) * len(class_weights)

  return jnp.mean(
      dice_loss(
          predictions,
          targets,
          class_weights=class_weights,
          smooth=smooth,
          apply_softmax=apply_softmax,
          reduction="none",
          ignore_background=ignore_background,
      )
  )

