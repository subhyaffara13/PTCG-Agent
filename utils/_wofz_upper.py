
def _wofz_upper(z: Array) -> Array:
  re = lax.real(z)
  L = lax.complex(_lax_const(re, _WOFZ_L), _lax_const(re, 0.))
  iz = lax.complex(lax.neg(lax.imag(z)), re)
  denom = L - iz
  Z = (L + iz) / denom
  p = jnp.polyval(jnp.asarray(_WOFZ_C, dtype=Z.dtype), Z)
  one_over_sqrtpi = lax.complex(_lax_const(re, 1. / np.sqrt(np.pi)), _lax_const(re, 0.))
  return 2 * p / (denom * denom) + one_over_sqrtpi / denom

