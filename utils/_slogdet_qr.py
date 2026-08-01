
def _slogdet_qr(a: Array) -> tuple[Array, Array]:
  # Implementation of slogdet using QR decomposition. One reason we might prefer
  # QR decomposition is that it is more amenable to a fast batched
  # implementation on TPU because of the lack of row pivoting.
  if jnp.issubdtype(lax.dtype(a), np.complexfloating):
    raise NotImplementedError("slogdet method='qr' not implemented for complex "
                              "inputs")
  n = a.shape[-1]
  a, taus = lax_linalg.geqrf(a)
  # The determinant of a triangular matrix is the product of its diagonal
  # elements. We are working in log space, so we compute the magnitude as the
  # the trace of the log-absolute values, and we compute the sign separately.
  a_diag = jnp.diagonal(a, axis1=-2, axis2=-1)
  log_abs_det = reductions.sum(ufuncs.log(ufuncs.abs(a_diag)), axis=-1)
  sign_diag = reductions.prod(ufuncs.sign(a_diag), axis=-1)
  # The determinant of a Householder reflector is -1. So whenever we actually
  # made a reflection (tau != 0), multiply the result by -1.
  sign_taus = reductions.prod(jnp.where(taus[..., :(n-1)] != 0, -1, 1), axis=-1).astype(sign_diag.dtype)
  return sign_diag * sign_taus, log_abs_det

