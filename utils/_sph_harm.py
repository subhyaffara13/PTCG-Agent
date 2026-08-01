
def _sph_harm(n: Array,
              m: Array,
              theta: Array,
              phi: Array,
              n_max: int) -> Array:
  """Computes the spherical harmonics."""

  cos_colatitude = jnp.cos(theta)

  legendre = _gen_associated_legendre(n_max, cos_colatitude, True)
  legendre_val = legendre.at[abs(m), n, jnp.arange(len(n))].get(mode="clip")

  angle = abs(m) * phi
  vandermonde = lax.complex(jnp.cos(angle), jnp.sin(angle))
  harmonics = lax.complex(legendre_val * jnp.real(vandermonde),
                          legendre_val * jnp.imag(vandermonde))

  # Negative order.
  harmonics = jnp.where(m < 0,
                        (-1.0)**abs(m) * jnp.conjugate(harmonics),
                        harmonics)

  return harmonics

