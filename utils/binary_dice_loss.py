
def binary_dice_loss(
    predictions: jax.typing.ArrayLike,
    targets: jax.typing.ArrayLike,
    *,
    smooth: jax.typing.ArrayLike = 1.,
    apply_sigmoid: bool = True,
) -> jax.Array:
  """Binary Dice Loss convenience function.

  Args:
      predictions: Logits of shape [...] or [..., 1].
      targets: Binary targets of shape [...] or [..., 1].
      smooth: Smoothing parameter.
      apply_sigmoid: Whether to apply sigmoid to predictions.

  Returns:
      Loss values of shape [...] (batch dimensions only).
  """
  # Ensure both have channel dimension
  if predictions.ndim == targets.ndim and predictions.shape[-1] != 1:  # pytype: disable=attribute-error  # jax-arraylike # noqa: E501
    predictions = predictions[..., None]
    targets = targets[..., None]

  return dice_loss(
      predictions,
      targets,
      smooth=smooth,
      apply_softmax=apply_sigmoid,
      reduction="mean",
  )

