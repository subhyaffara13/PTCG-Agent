
def _log_diff(log_p, log_q):
    return sc.logsumexp([log_p, log_q+np.pi*1j], axis=0)


def _log_diff(log_p, log_q):
    return special.logsumexp([log_p, log_q+np.pi*1j], axis=0)


def _log_diff(x, y):
  return logsumexp(
    jnp.array([x, y]),
    b=jnp.array([jnp.ones_like(x), -jnp.ones_like(y)]),
    axis=0
  )

