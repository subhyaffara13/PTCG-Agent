
def _slogdet_lu(a: Array) -> tuple[Array, Array]:
  """Sign and log(abs(det)) via LU. Custom JVP is required: (1) sign(det) is
  discontinuous at det=0 so standard autodiff is undefined; we use sign_dot=0
  for real and a consistent rule for complex. (2) d/dA log|det(A)| = trace(A⁻¹ Ȧ),
  which we implement explicitly; autodiff through det→abs→log would not yield
  this formula and is undefined at singular A."""
  dtype = lax.dtype(a)
  lu, pivot, _ = lax_linalg.lu(a)
  diag = jnp.diagonal(lu, axis1=-2, axis2=-1)
  is_zero = reductions.any(diag == jnp.array(0, dtype=dtype), axis=-1)
  iota = lax.expand_dims(jnp.arange(a.shape[-1], dtype=pivot.dtype),
                         range(pivot.ndim - 1))
  parity = reductions.count_nonzero(pivot != iota, axis=-1)
  if jnp.iscomplexobj(a):
    sign = reductions.prod(diag / ufuncs.abs(diag).astype(diag.dtype), axis=-1)
  else:
    sign = jnp.array(1, dtype=dtype)
    parity = parity + reductions.count_nonzero(diag < 0, axis=-1)
  sign = jnp.where(is_zero,
                  jnp.array(0, dtype=dtype),
                  sign * jnp.array(-2 * (parity % 2) + 1, dtype=dtype))
  logdet = jnp.where(
      is_zero, jnp.array(-np.inf, dtype=dtype),
      reductions.sum(ufuncs.log(ufuncs.abs(diag)).astype(dtype), axis=-1))
  return sign, ufuncs.real(logdet)

