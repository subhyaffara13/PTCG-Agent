
def _eigh_ascending(A):
  w, V = jnp.linalg.eigh(A)
  return w[::-1], V[:, ::-1]

