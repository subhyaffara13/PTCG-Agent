
def policy_gradient_loss(logits, *args):
  """rlax.policy_gradient_loss, but with sum(loss) and [T, B, ...] inputs."""
  # jax.experimental.host_callback.id_print(logits.shape)
  # print(logits.shape)
  mean_per_batch = jax.vmap(rlax.policy_gradient_loss, in_axes=1)(logits, *args)
  total_loss_per_batch = mean_per_batch * logits.shape[0]
  return jnp.sum(total_loss_per_batch)

