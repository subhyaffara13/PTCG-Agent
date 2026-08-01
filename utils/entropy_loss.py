
def entropy_loss(logits, *args):
  """rlax.entropy_loss, but with sum(loss) and [T, B, ...] inputs."""
  mean_per_batch = jax.vmap(rlax.entropy_loss, in_axes=1)(logits, *args)
  total_loss_per_batch = mean_per_batch * logits.shape[0]
  return jnp.sum(total_loss_per_batch)

