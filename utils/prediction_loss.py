
def prediction_loss(logits, labels):
  # print(logits.shape)  -> [T, B, num_preds]
  # print(labels.shape)  -> [T, B]
  mean_per_batch = jax.vmap(mean_pred_loss_without_batch, in_axes=1)(
      logits, labels
  )
  total_loss_per_batch = mean_per_batch * logits.shape[0]
  return jnp.sum(total_loss_per_batch)

