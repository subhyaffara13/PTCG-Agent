
def _algorithm_11_1_1(F: Array, T: Array) -> tuple[Array, Array]:
  # Algorithm 11.1.1 from Golub and Van Loan "Matrix Computations"
  N = T.shape[0]
  minden = jnp.abs(T[0, 0])

  def _outer_loop(p, F_minden):
    _, F, minden = lax.fori_loop(1, N-p+1, _inner_loop, (p, *F_minden))
    return F, minden

  def _inner_loop(i, p_F_minden):
    p, F, minden = p_F_minden
    j = i+p
    s = T[i-1, j-1] * (F[j-1, j-1] - F[i-1, i-1])
    T_row, T_col = T[i-1], T[:, j-1]
    F_row, F_col = F[i-1], F[:, j-1]
    ind = (jnp.arange(N) >= i) & (jnp.arange(N) < j-1)
    val = (jnp.where(ind, T_row, 0) @ jnp.where(ind, F_col, 0) -
            jnp.where(ind, F_row, 0) @ jnp.where(ind, T_col, 0))
    s = s + val
    den = T[j-1, j-1] - T[i-1, i-1]
    s = jnp.where(den != 0, s / den, s)
    F = F.at[i-1, j-1].set(s)
    minden = jnp.minimum(minden, jnp.abs(den))
    return p, F, minden

  return lax.fori_loop(1, N, _outer_loop, (F, minden))

