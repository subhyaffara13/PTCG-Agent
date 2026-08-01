
def sigmoid_binary_cross_entropy(
    logits,
    labels,
):
  """Computes element-wise sigmoid cross entropy given logits and labels.

  This function can be used for binary or multiclass classification (where each
  class is an independent binary prediction and different classes are not
  mutually exclusive e.g. predicting that an image contains both a cat
  and a dog.)

  Because this function is overloaded, please ensure your `logits` and `labels`
  are compatible with each other. If you're passing in binary `labels` (values
  in {0, 1}), ensure your `logits` correspond to class 1 only. If you're
  passing in per-class target probabilities or one-hot `labels`, please ensure
  your `logits` are also multiclass. Be particularly careful if you're relying
  on implicit broadcasting to reshape `logits` or `labels`.

  Args:
    logits: Each element is the unnormalized log probability of a binary
      prediction. See note about compatibility with `labels` above.
    labels: Binary labels whose values are {0,1} or multi-class target
      probabilities. See note about compatibility with `logits` above.

  Returns:
    cross entropy for each binary prediction, same shape as `logits`.

  References:
    Goodfellow et al, `Deep Learning
    <http://www.deeplearningbook.org/contents/prob.html>`_, 2016
  """
  utils.check_subdtype(logits, jnp.floating)
  labels = jnp.astype(labels, logits.dtype)  # pytype: disable=attribute-error  # jax-arraylike # noqa: E501
  log_p = jax.nn.log_sigmoid(logits)
  # log(1 - sigmoid(x)) = log_sigmoid(-x), the latter more numerically stable
  log_not_p = jax.nn.log_sigmoid(-logits)
  return -labels * log_p - (1.0 - labels) * log_not_p

