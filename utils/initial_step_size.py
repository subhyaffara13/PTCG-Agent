
def initial_step_size(fun, t0, y0, order, rtol, atol, f0):
  # Algorithm from:
  # E. Hairer, S. P. Norsett G. Wanner,
  # Solving Ordinary Differential Equations I: Nonstiff Problems, Sec. II.4.
  y0, f0 = promote_dtypes_inexact(y0, f0)
  dtype = y0.dtype

  scale = atol + jnp.abs(y0) * rtol
  d0 = jnp.linalg.norm(y0 / scale.astype(dtype))
  d1 = jnp.linalg.norm(f0 / scale.astype(dtype))

  h0 = jnp.where((d0 < 1e-5) | (d1 < 1e-5), 1e-6, 0.01 * d0 / d1)
  y1 = y0 + h0.astype(dtype) * f0
  f1 = fun(y1, t0 + h0)
  d2 = jnp.linalg.norm((f1 - f0) / scale.astype(dtype)) / h0

  h1 = jnp.where((d1 <= 1e-15) & (d2 <= 1e-15),
                jnp.maximum(1e-6, h0 * 1e-3),
                (0.01 / jnp.maximum(d1, d2)) ** (1. / (order + 1.)))

  return jnp.minimum(100. * h0, h1)

