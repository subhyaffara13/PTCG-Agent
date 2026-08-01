
def l2_norm(sample):
    return distance.pdist(sample).min()


def l2_norm(tree):
  """Compute the l2 norm of a pytree of arrays. Useful for weight decay."""
  leaves, _ = jax.tree.flatten(tree)
  return jnp.sqrt(sum(jnp.vdot(x, x) for x in leaves))

