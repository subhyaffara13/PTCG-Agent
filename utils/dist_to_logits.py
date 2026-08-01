
def dist_to_logits(dist):
  # dist[-1] = exp(logits[-1]) / Z = exp(0) / Z
  z = 1 / dist[-1]
  logits = jnp.log(dist[:-1] * z)
  return logits


def dist_to_logits(dist, eps=1e-8):
  # dist[-1] = exp(logits[-1]) / Z = exp(0) / Z
  z = 1 / jnp.clip(dist[-1], eps, 1.)
  logits = jnp.log(jnp.clip(dist[:-1] * z, eps, np.inf))
  return logits


def dist_to_logits(dist, eps=1e-8):
  # dist[-1] = exp(logits[-1]) / Z = exp(0) / Z
  z = 1 / jnp.clip(dist[-1], eps, 1.)
  logits = jnp.log(jnp.clip(dist[:-1] * z, eps, np.inf))
  return logits


def dist_to_logits(dist, eps=1e-8):
  # dist[-1] = exp(logits[-1]) / Z = exp(0) / Z
  z = 1 / jnp.clip(dist[-1], eps, 1.)
  logits = jnp.log(jnp.clip(dist[:-1] * z, eps, np.inf))
  return logits

