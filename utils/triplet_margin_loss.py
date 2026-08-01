
def triplet_margin_loss(
    anchor: Tensor,
    positive: Tensor,
    negative: Tensor,
    margin: float = 1.0,
    p: float = 2,
    eps: float = 1e-6,
    swap: bool = False,
    size_average: bool | None = None,
    reduce: bool | None = None,
    reduction: str = "mean",
) -> Tensor:
    r"""Compute the triplet loss between given input tensors and a margin greater than 0.

    See :class:`~torch.nn.TripletMarginLoss` for details.
    """
    if has_torch_function_variadic(anchor, positive, negative):
        return handle_torch_function(
            triplet_margin_loss,
            (anchor, positive, negative),
            anchor,
            positive,
            negative,
            margin=margin,
            p=p,
            eps=eps,
            swap=swap,
            size_average=size_average,
            reduce=reduce,
            reduction=reduction,
        )
    if size_average is not None or reduce is not None:
        reduction_enum = _Reduction.legacy_get_enum(size_average, reduce)
    else:
        reduction_enum = _Reduction.get_enum(reduction)
    if margin <= 0:
        raise ValueError(f"margin must be greater than 0, got {margin}")
    return torch.triplet_margin_loss(
        anchor, positive, negative, margin, p, eps, swap, reduction_enum
    )


def triplet_margin_loss(
    anchor: TensorLikeType,
    positive: TensorLikeType,
    negative: TensorLikeType,
    margin: float = 1.0,
    p: float = 2,
    eps: float = 1e-6,
    swap: bool = False,
    size_average: bool | None = None,
    reduce: bool | None = None,
    reduction: str = "mean",
) -> TensorLikeType:
    if size_average is not None or reduce is not None:
        # TODO: Raise exception instead of converting value.  This is only for
        # primTorch since it can drop support for deprecated arguments.
        # msg = "size_average and reduce args are deprecated, please use reduction argument."
        reduction = _get_string_reduction_arg(size_average=size_average, reduce=reduce)

    if margin <= 0:
        raise ValueError(f"margin must be greater than 0, got {margin}")

    # torch.nn.functional.triplet_margin_with_distance_loss has no ref defined
    # since it's a pure Python implementation.  Use this helper instead.
    return _triplet_margin_with_distance_loss(
        anchor=anchor,
        positive=positive,
        negative=negative,
        distance_function=lambda x, y: torch.pairwise_distance(x, y, p, eps),
        margin=margin,
        swap=swap,
        reduction=reduction,
    )


def triplet_margin_loss(
    anchors: jax.typing.ArrayLike,
    positives: jax.typing.ArrayLike,
    negatives: jax.typing.ArrayLike,
    axis: int = -1,
    norm_degree: jax.typing.ArrayLike = 2,
    margin: jax.typing.ArrayLike = 1.0,
    eps: jax.typing.ArrayLike = 1e-6,
) -> jax.Array:
  """Returns the triplet loss for a batch of embeddings.

  Examples:
    >>> import jax.numpy as jnp, optax
    >>> jnp.set_printoptions(precision=4)
    >>> anchors = jnp.array([[0.0, 0.0], [1.0, 1.0]])
    >>> positives = jnp.array([[0.1, 0.1], [1.1, 1.1]])
    >>> negatives = jnp.array([[1.0, 0.0], [0.0, 1.0]])
    >>> output = optax.losses.triplet_margin_loss(anchors, positives, negatives,
    ...                                           margin=1.0)
    >>> print(output)
    [0.1414 0.1414]

  Args:
    anchors: An array of anchor embeddings, with shape [batch, feature_dim].
    positives: An array of positive embeddings (similar to anchors), with
      shape [batch, feature_dim].
    negatives: An array of negative embeddings (dissimilar to anchors), with
      shape [batch, feature_dim].
    axis: The axis along which to compute the distances (default is -1).
    norm_degree: The norm degree for distance calculation (default is 2 for
      Euclidean distance).
    margin: The minimum margin by which the positive distance should be
      smaller than the negative distance.
    eps: A small epsilon value to ensure numerical stability in the distance
      calculation.

  Returns:
    Returns the computed triplet loss as an array.

  References:
      V. Balntas et al,
      `Learning shallow convolutional feature descriptors with triplet losses
      <https://bmva-archive.org.uk/bmvc/2016/papers/paper119/abstract119.pdf>`_,
      2016.
  """
  utils.check_subdtype(anchors, jnp.floating)
  utils.check_subdtype(positives, jnp.floating)
  utils.check_subdtype(negatives, jnp.floating)
  positive_distance = jnp.power(jnp.power(anchors - positives, norm_degree)
                                .sum(axis) + eps, 1 / norm_degree)
  negative_distance = jnp.power(jnp.power(anchors - negatives, norm_degree)
                                .sum(axis) + eps, 1 / norm_degree)
  loss = jnp.maximum(positive_distance - negative_distance + margin, 0)
  return loss

