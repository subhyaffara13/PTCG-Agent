
def _sici_approx(x: Array):
  # sici approximation valid for x >= 1E9
  si = (np.pi / 2) - jnp.cos(x) / x
  ci = jnp.sin(x) / x

  si = jnp.where(isposinf(x), np.pi / 2, si)
  ci = jnp.where(isposinf(x), 0.0, ci)

  return si, ci

