
def _sqrtm(A: ArrayLike) -> Array:
  T, Z = schur(A, output='complex')
  sqrt_T = _sqrtm_triu(T)
  return jnp.matmul(jnp.matmul(Z, sqrt_T, precision=lax.Precision.HIGHEST),
                    jnp.conj(Z.T), precision=lax.Precision.HIGHEST)

