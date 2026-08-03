from typing import Optional

def huber_loss(input, target, delta: float = 1.0):
    errors = torch.abs(input - target)  # shape (batch_size,)
    return torch.where(errors < delta, 0.5 * errors**2, errors * delta - (0.5 * delta**2))


def huber_loss(
    input: Tensor,
    target: Tensor,
    reduction: str = "mean",
    delta: float = 1.0,
    weight: Tensor | None = None,
) -> Tensor:
    r"""Compute the Huber loss, with optional weighting.

    Function uses a squared term if the absolute
    element-wise error falls below delta and a delta-scaled L1 term otherwise.

    When delta equals 1, this loss is equivalent to SmoothL1Loss.
    In general, Huber loss differs from SmoothL1Loss by a factor of delta (AKA beta in Smooth L1).

    See :class:`~torch.nn.HuberLoss` for details.

    Args:
        input (Tensor): Predicted values.
        target (Tensor): Ground truth values.
        reduction (str, optional): Specifies the reduction to apply to the output:
                                   'none' | 'mean' | 'sum'. 'mean': the mean of the output is taken.
                                   'sum': the output will be summed. 'none': no reduction will be applied.
                                   Default: 'mean'.
        delta (float, optional): The threshold at which to change between delta-scaled L1 and L2 loss. Default: 1.0.
        weight (Tensor, optional): Weights for each sample. Default: None.

    Returns:
        Tensor: Huber loss (optionally weighted).
    """
    if has_torch_function_variadic(input, target, weight):
        return handle_torch_function(
            huber_loss,
            (input, target, weight),
            input,
            target,
            reduction=reduction,
            delta=delta,
            weight=weight,
        )

    if target.size() != input.size():
        warnings.warn(
            f"Using a target size ({target.size()}) that is different to the input size ({input.size()}). "
            "This will likely lead to incorrect results due to broadcasting. "
            "Please ensure they have the same size.",
            stacklevel=2,
        )

    expanded_input, expanded_target = torch.broadcast_tensors(input, target)

    if weight is None:
        # Use the optimized C++ backend for standard Huber loss
        return torch._C._nn.huber_loss(
            expanded_input,
            expanded_target,
            # pyrefly: ignore [bad-argument-type]
            _Reduction.get_enum(reduction),
            delta,
        )
    else:
        if weight.size() != input.size():
            raise ValueError("Weights and input must have the same size.")

        # Calculate the unweighted loss first
        unweighted_loss = torch._C._nn.huber_loss(
            expanded_input,
            expanded_target,
            # pyrefly: ignore [bad-argument-type]
            _Reduction.get_enum("none"),
            delta,
        )

        # Apply weight to the unweighted loss
        weighted_loss = unweighted_loss * weight

        if reduction == "none":
            return weighted_loss
        elif reduction == "sum":
            return torch.sum(weighted_loss)
        elif reduction == "mean":
            return weighted_loss.mean()
        else:
            raise ValueError(
                f"Invalid reduction mode: {reduction}. Expected one of 'none', 'mean', 'sum'."
            )


def huber_loss(
    input: TensorLikeType,
    target: TensorLikeType,
    reduction: str | int = "mean",
    delta: float = 1.0,
) -> TensorLikeType:
    """
    Reference implementation of torch.nn.functional.huber_loss
    """
    if type(reduction) is int:
        reduction = _reduction_int_to_str(reduction)
    _check_reduction_value(reduction)  # type: ignore[arg-type]
    torch._check(
        delta > 0,
        lambda: "huber_loss does not support non-positive values for delta.",
    )
    z = (input - target).abs()
    loss = torch.where(z < delta, 0.5 * z * z, delta * (z - 0.5 * delta))
    return _apply_loss_reduction(loss, reduction)  # type: ignore[arg-type]


def huber_loss(
    predictions: jax.typing.ArrayLike,
    targets: Optional[jax.typing.ArrayLike] = None,
    *,
    delta: jax.typing.ArrayLike = 1.0,
) -> jax.Array:
  """Huber loss, similar to L2 loss close to zero, L1 loss away from zero.

  If gradient descent is applied to the `huber loss`, it is equivalent to
  clipping gradients of an `l2_loss` to `[-delta, delta]` in the backward pass.

  Args:
    predictions: a vector of arbitrary shape `[...]`.
    targets: a vector with shape broadcastable to that of `predictions`; if not
      provided then it is assumed to be a vector of zeros.
    delta: the bounds for the huber loss transformation, defaults at 1.

  Returns:
    elementwise huber losses, with the same shape of `predictions`.

  References:
    `Huber loss <https://en.wikipedia.org/wiki/Huber_loss>`_, Wikipedia.
  """
  utils.check_subdtype(predictions, jnp.floating)
  errors = (predictions - targets) if (targets is not None) else predictions
  # 0.5 * err^2                  if |err| <= d
  # 0.5 * d^2 + d * (|err| - d)  if |err| > d
  abs_errors = jnp.abs(errors)
  quadratic = jnp.minimum(abs_errors, delta)
  # Same as max(abs_x - delta, 0) but avoids potentially doubling gradient.
  linear = abs_errors - quadratic
  return 0.5 * quadratic**2 + delta * linear

