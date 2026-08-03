from typing import Union

def softmax_cross_entropy_with_integer_labels(
    logits: jax.typing.ArrayLike,
    labels: jax.typing.ArrayLike,
    axis: Union[int, tuple[int, ...]] = -1,
    where: Union[jax.typing.ArrayLike, None] = None,
) -> jax.Array:
  r"""Computes softmax cross entropy between the logits and integer labels.

  This loss is useful for classification problems with integer labels that are
  not one-hot encoded. This loss is also known as categorical cross entropy.

  Let :math:`x` denote the ``logits`` array of size ``[batch_size,
  num_classes]`` and :math:`y` denote the ``labels`` array of size
  ``[batch_size]``. Then this function returns a vector
  :math:`\sigma` of size ``[batch_size]`` defined as:

  .. math::
    \sigma_i =
    \log\left(\frac{\exp(x_{i y_i})}{\sum_j
    \exp(x_{i j})}\right)\,.

  Args:
    logits: Unnormalized log probabilities, with shape ``[batch_size,
      num_classes]``.
    labels: Integers specifying the correct class for each input, with shape
      ``[batch_size]``. Class labels are assumed to be between 0 and
      ``num_classes - 1`` inclusive.
    axis: Axis or axes along which to compute. If a tuple of axes is passed
      then ``num_classes`` must match the total number of elements in ``axis``
      dimensions and a label is interpreted as a flat index in a ``logits``
      slice of shape ``logits[axis]``.
    where: Elements to include in the computation of shape ``[batch_size]``
      or logits.shape.

  Returns:
    Cross-entropy between each prediction and the corresponding target
    distributions, with shape ``[batch_size]``.

  Examples:
    >>> import optax
    >>> import jax.numpy as jnp
    >>> jnp.set_printoptions(precision=4)
    >>> # example: batch_size = 2, num_classes = 3
    >>> logits = jnp.array([[1.2, -0.8, -0.5], [0.9, -1.2, 1.1]])
    >>> labels = jnp.array([0, 1])
    >>> print(optax.softmax_cross_entropy_with_integer_labels(logits, labels))
    [0.2761 2.9518]

    >>> import jax.numpy as jnp
    >>> import numpy as np
    >>> import optax
    >>> jnp.set_printoptions(precision=4)
    >>> # example: batch_size = (1, 2), num_classes = 12 (i.e. 3 * 4)
    >>> shape = (1, 2, 3, 4)
    >>> logits = jnp.arange(np.prod(shape), dtype=jnp.float32).reshape(shape)
    >>> # elements indices in slice of shape (3, 4)
    >>> ix = jnp.array([[1, 2]])
    >>> jx = jnp.array([[1, 3]])
    >>> labels = jnp.ravel_multi_index((ix, jx), shape[2:])
    >>> cross_entropy = optax.softmax_cross_entropy_with_integer_labels(
    ...     logits, labels, axis=(2, 3))
    >>> print(cross_entropy)
    [[6.4587 0.4587]]

  References:
    `Cross-entropy Loss <https://en.wikipedia.org/wiki/Cross-entropy>`_,
    Wikipedia

    `Multinomial Logistic Regression
    <https://en.wikipedia.org/wiki/Multinomial_logistic_regression>`_, Wikipedia

  .. seealso:: This function is similar to
    :func:`optax.losses.softmax_cross_entropy`, but accepts integer labels
    instead of one-hot labels.

  .. versionchanged:: 0.2.4
    Added ``axis`` and ``where`` arguments.
  """
  utils.check_subdtype(logits, jnp.floating)
  utils.check_subdtype(labels, jnp.integer)
  if where is not None and where.ndim != logits.ndim:  # pytype: disable=attribute-error  # jax-arraylike # noqa: E501
    where = jnp.expand_dims(where, axis)
  if isinstance(axis, int):
    axis = canonicalize_axis(axis, logits.ndim)  # pytype: disable=attribute-error  # jax-arraylike # noqa: E501
  elif isinstance(axis, tuple):
    # Move all "feature" dimensions to the end preserving axis ordering and
    # subsequent flattening "feature" dimensions to a single one.
    logit_axis = canonicalize_axes(axis, logits.ndim)  # pytype: disable=attribute-error  # jax-arraylike # noqa: E501
    batch_axis = tuple(x for x in range(logits.ndim) if x not in logit_axis)  # pytype: disable=attribute-error  # jax-arraylike # noqa: E501
    axis = len(batch_axis)
    logits = logits.transpose(batch_axis + logit_axis)  # pytype: disable=attribute-error  # jax-arraylike # noqa: E501
    logits = logits.reshape(logits.shape[:len(batch_axis)] + (-1,))
    if where is not None:
      where = where.transpose(batch_axis + logit_axis)  # pytype: disable=attribute-error  # jax-arraylike # noqa: E501
      where = where.reshape(where.shape[:len(batch_axis)] + (-1,))
  else:
    raise ValueError('Keyword argument \'axis\' must be of type \'int\' or '
                     f'\'tuple[int, ...]\' but actual type is {type(axis)}.')
  # This is like jnp.take_along_axis(jax.nn.log_softmax(...), ...) except that
  # we avoid subtracting the normalizer from all values, just from the values
  # for the correct labels.
  label_logits = jnp.take_along_axis(
      logits, jnp.expand_dims(labels, axis), axis=axis
  ).take(0, axis=axis)
  log_normalizers = jax.nn.logsumexp(logits, axis=axis, where=where)
  out = log_normalizers - label_logits
  if where is not None:
    out = jnp.where(jnp.any(where, axis), out, 0.0)
  return out

