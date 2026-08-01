
def softmax_cross_entropy(
    logits: jax.typing.ArrayLike,
    labels: jax.typing.ArrayLike,
    axis: Union[int, tuple[int, ...], None] = -1,
    where: Union[jax.typing.ArrayLike, None] = None,
) -> jax.Array:
  r"""Computes the softmax cross entropy between sets of logits and labels.

  This loss function is commonly used for multi-class classification tasks. It
  measures the dissimilarity between the predicted probability distribution
  (obtained by applying the softmax function to the logits) and the true
  probability distribution (represented by the one-hot encoded labels).
  This loss is also known as categorical cross entropy.

  Let :math:`x` denote the ``logits`` array of size ``[batch_size,
  num_classes]`` and :math:`y` denote the ``labels`` array of size
  ``[batch_size, num_classes]``. Then this function returns a vector
  :math:`\sigma` of size ``[batch_size]`` defined as:

  .. math::
    \sigma_i =
    - \sum_j y_{i j} \log\left(\frac{\exp(x_{i j})}{\sum_k
    \exp(x_{i k})}\right) \,.

  Args:
    logits: Unnormalized log probabilities, with shape ``[batch_size,
      num_classes]``.
    labels: One-hot encoded labels, with shape `[batch_size, num_classes]`. Each
      row represents the true class distribution for a single example.
    axis: Axis or axes along which to compute.
    where: Elements to include in the computation of shape ``[batch_size]`` or
      logits.shape.

  Returns:
    Cross-entropy between each prediction and the corresponding target
    distributions, with shape ``[batch_size]``.

  Examples:
    >>> import optax
    >>> import jax.numpy as jnp
    >>> jnp.set_printoptions(precision=4)
    >>> # example: batch_size = 2, num_classes = 3
    >>> logits = jnp.array([[1.2, -0.8, -0.5], [0.9, -1.2, 1.1]])
    >>> labels = jnp.array([[1.0, 0.0, 0.0], [0.0, 1.0, 0.0]])
    >>> print(optax.softmax_cross_entropy(logits, labels))
    [0.2761 2.9518]

  References:
    `Cross-entropy Loss <https://en.wikipedia.org/wiki/Cross-entropy>`_,
    Wikipedia

    `Multinomial Logistic Regression
    <https://en.wikipedia.org/wiki/Multinomial_logistic_regression>`_, Wikipedia

  .. seealso::
    This function is similar to
    :func:`optax.losses.softmax_cross_entropy_with_integer_labels`,
    but accepts one-hot labels instead of integer labels.

    :func:`optax.losses.safe_softmax_cross_entropy` provides an alternative
    implementation that differs on how ``logits=-inf`` are handled.

  .. versionchanged:: 0.2.4
    Added ``axis`` and ``where`` arguments.
  """
  utils.check_subdtype(logits, jnp.floating)
  if where is not None and where.ndim != logits.ndim:  # pytype: disable=attribute-error  # jax-arraylike # noqa: E501
    where = jnp.expand_dims(where, axis)
  log_probs = jax.nn.log_softmax(logits, axis, where)
  return -(labels * log_probs).sum(axis, where=where)

