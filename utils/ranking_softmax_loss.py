
def ranking_softmax_loss(
    logits: jax.typing.ArrayLike,
    labels: jax.typing.ArrayLike,
    *,
    where: Optional[jax.typing.ArrayLike] = None,
    weights: Optional[jax.typing.ArrayLike] = None,
    reduce_fn: Optional[Callable[..., jax.typing.ArrayLike]] = jnp.mean
) -> jax.Array:
  r"""Ranking softmax loss.

  Definition:

  .. math::
      \ell(s, y) = -\sum_i y_i \log \frac{\exp(s_i)}{\sum_j \exp(s_j)}

  Args:
    logits: A ``[..., list_size]``-:class:`~jax.Array`, indicating the score of
      each item.
    labels: A ``[..., list_size]``-:class:`~jax.Array`, indicating the relevance
      label for each item.
    where: An optional ``[..., list_size]``-:class:`~jax.Array`, indicating
      which items are valid for computing the loss. Items for which this is
      False will be ignored when computing the loss.
    weights: An optional ``[..., list_size]``-:class:`~jax.Array`, indicating
      the weight for each item.
    reduce_fn: An optional function that reduces the loss values. Can be
      :func:`jax.numpy.sum` or :func:`jax.numpy.mean`. If ``None``, no reduction
      is performed.

  Returns:
    The ranking softmax loss.
  """
  utils.check_subdtype(logits, jnp.floating)
  labels = labels.astype(logits.dtype)  # pytype: disable=attribute-error  # jax-arraylike # noqa: E501

  # Applies mask so that masked elements do not count towards the loss.
  if where is not None:
    labels = jnp.where(where, labels, jnp.zeros_like(labels))
    logits = jnp.where(where, logits, -jnp.ones_like(logits) * jnp.inf)

  # Apply weights to labels.
  if weights is not None:
    labels *= weights

  # Scales labels and logits to match the cross entropy loss.
  logits_log_softmax = jax.nn.log_softmax(logits, axis=-1)

  # Computes per-element cross entropy.
  softmax_cross_entropy = labels * logits_log_softmax

  # Reduces softmax cross-entropy loss.
  loss = -jnp.sum(softmax_cross_entropy, axis=-1, where=where)

  # Setup mask to ignore lists with only invalid items in reduce_fn.
  if where is not None:
    where = jnp.any(where, axis=-1)

  return _safe_reduce(loss, where=where, reduce_fn=reduce_fn)

