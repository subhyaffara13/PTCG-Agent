
def _complex_loggamma(z: Array) -> Array:
  """Principal-branch log-gamma for complex arguments via Lanczos approximation.

  Uses the reflection formula for Re(z) < 0.5.
  """
  assert dtypes.issubdtype(z.dtype, np.complexfloating)

  # Reflection: for Re(z) < 0.5, use Gamma(z) = pi / (sin(pi*z) * Gamma(1-z))
  needs_reflection = jnp.real(z) < 0.5
  z_lanczos = jnp.where(needs_reflection, 1.0 - z, z)

  # Lanczos approximation: Ag(z) = c[0] + sum(c[k] / (z + k - 1), k=1..N-1)
  zz = z_lanczos - 1.0
  coeffs = jnp.asarray(_LANCZOS_COEFFS, dtype=z.dtype)
  ks = lax.expand_dims(jnp.arange(1, 9, dtype=z.dtype), tuple(range(zz.ndim)))
  ag = coeffs[0] + jnp.sum(
      lax.expand_dims(coeffs[1:], tuple(range(zz.ndim)))
      / (lax.expand_dims(zz, (zz.ndim,)) + ks), axis=-1)

  t = zz + _LANCZOS_G + 0.5
  half_log2pi = jnp.asarray(0.5 * np.log(2.0 * np.pi), dtype=z.dtype)
  log_gamma_lanczos = (
      half_log2pi
      + (zz + 0.5) * jnp.log(t)
      - t
      + jnp.log(ag)
  )

  # Mask z to a safe value in the reflection branch so the unselected
  # path never produces NaN (which would contaminate gradients via
  # jnp.where's VJP: 0 * NaN = NaN in IEEE 754).
  z_safe = jnp.where(needs_reflection, z, jnp.full_like(z, 0.5))
  reflected = (
      jnp.log(jnp.asarray(np.pi, dtype=z.dtype))
      - jnp.log(jnp.sin(np.pi * z_safe))
      - log_gamma_lanczos
  )

  return jnp.where(needs_reflection, reflected, log_gamma_lanczos)

