from typing import Optional

def sigmoid_focal_loss(inputs, targets, num_boxes, alpha: float = 0.25, gamma: float = 2):
    """
    Loss used in RetinaNet for dense detection: https://huggingface.co/papers/1708.02002.

    Args:
        inputs (`torch.FloatTensor` of arbitrary shape):
            The predictions for each example.
        targets (`torch.FloatTensor` with the same shape as `inputs`)
            A tensor storing the binary classification label for each element in the `inputs` (0 for the negative class
            and 1 for the positive class).
        alpha (`float`, *optional*, defaults to `0.25`):
            Optional weighting factor in the range (0,1) to balance positive vs. negative examples.
        gamma (`int`, *optional*, defaults to `2`):
            Exponent of the modulating factor (1 - p_t) to balance easy vs hard examples.

    Returns:
        Loss tensor
    """
    prob = inputs.sigmoid()
    ce_loss = nn.functional.binary_cross_entropy_with_logits(inputs, targets, reduction="none")
    # add modulating factor
    p_t = prob * targets + (1 - prob) * (1 - targets)
    loss = ce_loss * ((1 - p_t) ** gamma)

    if alpha >= 0:
        alpha_t = alpha * targets + (1 - alpha) * (1 - targets)
        loss = alpha_t * loss

    return loss.mean(1).sum() / num_boxes


def sigmoid_focal_loss(
    inputs: torch.Tensor,
    targets: torch.Tensor,
    num_boxes: int,
    alpha: float = 0.25,
    gamma: float = 2,
):
    """
    Loss used in RetinaNet for dense detection: https://huggingface.co/papers/1708.02002.

    Args:
        inputs (`torch.FloatTensor` of arbitrary shape):
            The predictions for each example.
        targets (`torch.FloatTensor` with the same shape as `inputs`)
            A tensor storing the binary classification label for each element in the `inputs` (0 for the negative class
            and 1 for the positive class).
        num_boxes (`int`):
            The total number of boxes in the batch.
        alpha (`float`, *optional*, defaults to 0.25):
            Optional weighting factor in the range (0,1) to balance positive vs. negative examples.
        gamma (`int`, *optional*, defaults to 2):
            Exponent of the modulating factor (1 - p_t) to balance easy vs hard examples.

    Returns:
        Loss tensor
    """
    prob = inputs.sigmoid()
    ce_loss = nn.functional.binary_cross_entropy_with_logits(inputs, targets, reduction="none")
    # add modulating factor
    p_t = prob * targets + (1 - prob) * (1 - targets)
    loss = ce_loss * ((1 - p_t) ** gamma)

    if alpha >= 0:
        alpha_t = alpha * targets + (1 - alpha) * (1 - targets)
        loss = alpha_t * loss

    return loss.sum() / num_boxes


def sigmoid_focal_loss(
    inputs: Tensor, labels: Tensor, num_masks: int, alpha: float = 0.25, gamma: float = 2
) -> Tensor:
    r"""
    Focal loss proposed in [Focal Loss for Dense Object Detection](https://huggingface.co/papers/1708.02002) originally used in
    RetinaNet. The loss is computed as follows:

    $$ \mathcal{L}_{\text{focal loss} = -(1 - p_t)^{\gamma}\log{(p_t)} $$

    where \\(CE(p_t) = -\log{(p_t)}}\\), CE is the standard Cross Entropy Loss

    Please refer to equation (1,2,3) of the paper for a better understanding.

    Args:
        inputs (`torch.Tensor`):
            A float tensor of arbitrary shape.
        labels (`torch.Tensor`):
            A tensor with the same shape as inputs. Stores the binary classification labels for each element in inputs
            (0 for the negative class and 1 for the positive class).
        num_masks (`int`):
            The number of masks present in the current batch, used for normalization.
        alpha (float, *optional*, defaults to 0.25):
            Weighting factor in range (0,1) to balance positive vs negative examples.
        gamma (float, *optional*, defaults to 2.0):
            Exponent of the modulating factor \\(1 - p_t\\) to balance easy vs hard examples.

    Returns:
        `torch.Tensor`: The computed loss.
    """
    criterion = nn.BCEWithLogitsLoss(reduction="none")
    probs = inputs.sigmoid()
    cross_entropy_loss = criterion(inputs, labels)
    p_t = probs * labels + (1 - probs) * (1 - labels)
    loss = cross_entropy_loss * ((1 - p_t) ** gamma)

    if alpha >= 0:
        alpha_t = alpha * labels + (1 - alpha) * (1 - labels)
        loss = alpha_t * loss

    loss = loss.mean(1).sum() / num_masks
    return loss


def sigmoid_focal_loss(
    inputs: Tensor, labels: Tensor, num_masks: int, alpha: float = 0.25, gamma: float = 2
) -> Tensor:
    r"""
    Focal loss proposed in [Focal Loss for Dense Object Detection](https://huggingface.co/papers/1708.02002) originally used in
    RetinaNet. The loss is computed as follows:

    $$ \mathcal{L}_{\text{focal loss} = -(1 - p_t)^{\gamma}\log{(p_t)} $$

    where \\(CE(p_t) = -\log{(p_t)}}\\), CE is the standard Cross Entropy Loss

    Please refer to equation (1,2,3) of the paper for a better understanding.

    Args:
        inputs (`torch.Tensor`):
            A float tensor of arbitrary shape.
        labels (`torch.Tensor`):
            A tensor with the same shape as inputs. Stores the binary classification labels for each element in inputs
            (0 for the negative class and 1 for the positive class).
        num_masks (`int`):
            The number of masks present in the current batch, used for normalization.
        alpha (float, *optional*, defaults to 0.25):
            Weighting factor in range (0,1) to balance positive vs negative examples.
        gamma (float, *optional*, defaults to 2.0):
            Exponent of the modulating factor \\(1 - p_t\\) to balance easy vs hard examples.

    Returns:
        `torch.Tensor`: The computed loss.
    """
    criterion = nn.BCEWithLogitsLoss(reduction="none")
    probs = inputs.sigmoid()
    cross_entropy_loss = criterion(inputs, labels)
    p_t = probs * labels + (1 - probs) * (1 - labels)
    loss = cross_entropy_loss * ((1 - p_t) ** gamma)

    if alpha >= 0:
        alpha_t = alpha * labels + (1 - alpha) * (1 - labels)
        loss = alpha_t * loss

    loss = loss.mean(1).sum() / num_masks
    return loss


def sigmoid_focal_loss(
    logits: jax.typing.ArrayLike,
    labels: jax.typing.ArrayLike,
    *,
    alpha: Optional[jax.typing.ArrayLike] = None,
    gamma: jax.typing.ArrayLike = 2.0,
) -> jax.Array:
  r"""Sigmoid focal loss with numerical stability improvements.

  The focal loss is a dynamically scaled cross entropy loss, where the scaling
  factor decays to zero as confidence in the correct class increases. This
  addresses class imbalance by down-weighting easy examples and focusing on
  hard examples.

  This implementation uses log-space computation for the focal weight
  :math:`(1-p_t)^\gamma` to ensure numerical stability, especially for
  :math:`\gamma < 2` and extreme logit values.

  The loss is defined as:

  .. math::
    FL(p_t) = -\alpha_t (1-p_t)^\gamma \log(p_t)

  where :math:`p_t` is the predicted probability of the correct class:

  .. math::
    p_t = \begin{cases}
      p & \text{if } y = 1 \\
      1-p & \text{if } y = 0
    \end{cases}

  and :math:`\alpha_t` is the weighting factor:

  .. math::
    \alpha_t = \begin{cases}
      \alpha & \text{if } y = 1 \\
      1-\alpha & \text{if } y = 0
    \end{cases}

  Args:
    logits: Array of unnormalized log probabilities, with shape `[..., ]`.
      The predictions for each example.
    labels: Array of labels with shape broadcastable to `logits`. Can be:
      - Binary labels `{0, 1}` for binary classification
      - Continuous labels `[0, 1]` for soft targets or label smoothing
    alpha: (optional) Weighting factor in range `(0, 1)` to balance positive vs
      negative examples. Default `None` (no weighting).
    gamma: Exponent of the modulating factor `(1 - p_t)`. Higher values focus
      more on hard examples. Default `2.0`.

  Returns:
    Focal loss values with shape identical to `logits`.

  References:
    Lin et al, `Focal Loss for Dense Object Detection
    <https://arxiv.org/abs/1708.02002>`_, 2017

  .. versionchanged:: 0.2.5
    Added numerical stability improvements using log-space computation.
    Added support for continuous labels in `[0, 1]`.
  """
  utils.check_subdtype(logits, jnp.floating)
  labels = jnp.astype(labels, logits.dtype)  # pytype: disable=attribute-error  # jax-arraylike # noqa: E501

  # Cross-entropy loss
  ce_loss = sigmoid_binary_cross_entropy(logits, labels)

  # Compute log(1-p_t) using logsumexp unconditionally
  log_p = jax.nn.log_sigmoid(logits)
  log_q = jax.nn.log_sigmoid(-logits)

  log_one_minus_p_t = jax.scipy.special.logsumexp(
      jnp.stack([log_p, log_q], axis=-1),
      axis=-1,
      b=jnp.stack([1 - labels, labels], axis=-1)
  )

  # Focal weight and final loss
  focal_weight = jnp.exp(gamma * log_one_minus_p_t)
  loss = ce_loss * focal_weight

  # Alpha weighting
  if alpha is None:
    return loss
  weighted = (alpha * labels + (1.0 - alpha) * (1.0 - labels)) * loss
  return weighted

