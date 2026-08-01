
def _eig_vec_jvp(dot, w, v, da):
  # Nondegenerate perturbation theory, see e.g. Sec 3.1 of
  # https://people.maths.ox.ac.uk/gilesm/files/NA-08-01.pdf
  # The eigenvalue equation A v_j = w_j v_j fixes v_j only up to a (complex)
  # scalar. LAPACK's geev fixes that scalar by normalising each v_j to have unit
  # 2-norm and real largest-magnitude component, and we differentiate through
  # that choice. See https://github.com/jax-ml/jax/issues/2748 for discussion.
  n = w.shape[-1]
  eye_n = lax._eye(w.dtype, (n, n))
  with config.numpy_rank_promotion('allow'):
    Fmat = lax.reciprocal(eye_n + w[..., None, :] - w[..., None]) - eye_n
  P = dot(_solve(v, da), v)
  dw = _extract_diagonal(P)
  U = dot(v, Fmat * P)
  # The eigenvalue equation gives dv_j = u_j + c_j v_j with c_j free; the two
  # real LAPACK normalisation constraints fix c_j to
  #   c_j = -Re(v_j* . u_j) - i Im(u_{k_j j}) / v_{k_j j},  k_j = argmax_i |v_ij|.
  k = lax.argmax(lax.abs(v), axis=v.ndim - 2, index_dtype=np.int32)
  mask = (lax.broadcasted_iota(np.int32, v.shape, v.ndim - 2)
          == lax.expand_dims(k, (v.ndim - 2,))).astype(v.dtype)
  c = lax.complex(-(v.conj() * U).sum(-2).real,
                  -(mask * U).sum(-2).imag / (mask * v).sum(-2).real)
  return dw, U + v * lax.expand_dims(c, (v.ndim - 2,))

