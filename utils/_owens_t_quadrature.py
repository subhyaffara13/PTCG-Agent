
def _owens_t_quadrature(h, a):
  quad_pts = jnp.expand_dims(_OWENS_T_QUAD_PTS, tuple(range(a.ndim)))
  r = jnp.square(a)[..., None] * quad_pts
  integrand = jnp.exp(-0.5 * jnp.square(h)[..., None] * (1. + r)) / (1. + r)
  return a * (integrand @ _OWENS_T_QUAD_WTS)

