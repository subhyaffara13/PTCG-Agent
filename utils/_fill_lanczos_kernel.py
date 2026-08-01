
def _fill_lanczos_kernel(radius, x):
  y = radius * jnp.sin(np.pi * x) * jnp.sin(np.pi * x / radius)
  #  out = y / (np.pi ** 2 * x ** 2) where x >1e-3, 1 otherwise
  out = jnp.where(x > 1e-3, jnp.divide(y, jnp.where(x != 0, np.pi**2 * x**2, 1)), 1)
  return jnp.where(x > radius, 0., out)

