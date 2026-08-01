
def mean_pred_loss_without_batch(
    logits_t: chex.Array,
    labels: chex.Array,
) -> chex.Array:
  """Mean prediction loss without batch dimension."""
  chex.assert_rank([logits_t, labels], [2, 1])
  chex.assert_type([logits_t, labels], [float, int])
  labels_one_hot = jax.nn.one_hot(labels, logits_t.shape[-1])
  softmax_xent = -jnp.sum(labels_one_hot * jax.nn.log_softmax(logits_t))
  softmax_xent /= labels.shape[0]
  return softmax_xent

