
def _rsf2csf_2d(T: Array, Z: Array) -> tuple[Array, Array]:
  T, Z = promote_dtypes_complex(T, Z)
  eps = dtypes.finfo(T.dtype).eps
  N = T.shape[0]

  if N == 1:
    return T, Z

  def _update_T_Z(m, T, Z):
    mu = jnp_linalg.eigvals(lax.dynamic_slice(T, (m-1, m-1), (2, 2))) - T[m, m]
    r = jnp_linalg.norm(jnp.array([mu[0], T[m, m-1]])).astype(T.dtype)
    c = mu[0] / r
    s = T[m, m-1] / r
    G = jnp.array([[c.conj(), s], [-s, c]], dtype=T.dtype)

    T_rows = lax.dynamic_slice_in_dim(T, m-1, 2, axis=0)
    col_mask = jnp.arange(N) >= m-1
    G_dot_T_zeroed_cols = G @ jnp.where(col_mask, T_rows, 0)
    T_rows_new = jnp.where(~col_mask, T_rows, G_dot_T_zeroed_cols)
    T = lax.dynamic_update_slice_in_dim(T, T_rows_new, m-1, axis=0)

    T_cols = lax.dynamic_slice_in_dim(T, m-1, 2, axis=1)
    row_mask = jnp.arange(N)[:, np.newaxis] < m+1
    T_zeroed_rows_dot_GH = jnp.where(row_mask, T_cols, 0) @ G.conj().T
    T_cols_new = jnp.where(~row_mask, T_cols, T_zeroed_rows_dot_GH)
    T = lax.dynamic_update_slice_in_dim(T, T_cols_new, m-1, axis=1)

    Z_cols = lax.dynamic_slice_in_dim(Z, m-1, 2, axis=1)
    Z = lax.dynamic_update_slice_in_dim(Z, Z_cols @ G.conj().T, m-1, axis=1)
    return T, Z

  def _rsf2csf_iter(i, TZ):
    m = N-i
    T, Z = TZ
    T, Z = lax.cond(
      jnp.abs(T[m, m-1]) > eps*(jnp.abs(T[m-1, m-1]) + jnp.abs(T[m, m])),
      _update_T_Z,
      lambda m, T, Z: (T, Z),
      m, T, Z)
    T = T.at[m, m-1].set(0.0)
    return T, Z

  return lax.fori_loop(1, N, _rsf2csf_iter, (T, Z))

