from typing import Union

def poly_loss_cross_entropy(
    logits: jax.typing.ArrayLike,
    labels: jax.typing.ArrayLike,
    *,
    epsilon: jax.typing.ArrayLike = 2.0,
    axis: Union[int, tuple[int, ...], None] = -1,
    where: Union[jax.typing.ArrayLike, None] = None,
) -> jax.Array:
  r"""Computes PolyLoss between logits and labels.

  The PolyLoss is a loss function that decomposes commonly
  used classification loss functions into a series of weighted
  polynomial bases. It is inspired by the Taylor expansion of
  cross-entropy loss and focal loss in the bases of :math:`(1 - P_t)^j`.

  .. math::
    L_{Poly} = \sum_1^\infty \alpha_j \cdot (1 - P_t)^j \\
    L_{Poly-N} = (\epsilon_1 + 1) \cdot (1 - P_t) + \ldots + \\
    (\epsilon_N + \frac{1}{N}) \cdot (1 - P_t)^N +
    \frac{1}{N + 1} \cdot (1 - P_t)^{N + 1} + \ldots = \\
    - \log(P_t) + \sum_{j = 1}^N \epsilon_j \cdot (1 - P_t)^j

  This function provides a simplified version of :math:`L_{Poly-N}`
  with only the coefficient of the first polynomial term being changed.

  Args:
    logits: Unnormalized log probabilities, with shape `[..., num_classes]`.
    labels: Valid probability distributions (non-negative, sum to 1), e.g. a
      one hot encoding specifying the correct class for each input;
      must have a shape broadcastable to `[..., num_classes]`.
    epsilon: The coefficient of the first polynomial term.
      According to the paper, the following values are recommended:
      - For the ImageNet 2d image classification, epsilon = 2.0.
      - For the 2d Instance Segmentation and object detection, epsilon = -1.0.
      - It is also recommended to adjust this value based on the task, e.g. by
      using grid search.
    axis: Axis or axes along which to compute.
    where: Elements to include in the computation.

  Returns:
    Poly loss between each prediction and the corresponding target
    distributions, with shape `[...]`.

  References:
    Leng et al, `PolyLoss: A Polynomial Expansion Perspective of Classification
    Loss Functions <https://arxiv.org/pdf/2204.12511.pdf>`_, 2022

  .. versionchanged:: 0.2.4
    Added ``axis`` and ``where`` arguments.
  """
  utils.check_subdtype(logits, jnp.floating)
  utils.check_subdtype(labels, jnp.floating)
  p = jax.nn.softmax(logits, axis=axis, where=where)
  one_minus_pt = jnp.sum(labels * (1 - p), axis=axis, where=where)
  cross_entropy = softmax_cross_entropy(
      logits=logits, labels=labels, axis=axis, where=where
  )
  return cross_entropy + epsilon * one_minus_pt

