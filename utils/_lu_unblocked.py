
def _lu_unblocked(a):
  """Unblocked LU decomposition, as a rolled loop."""
  m, n = a.shape
  def body(k, state):
    pivot, perm, a = state
    m_idx = lax.iota('int32', m)
    n_idx = lax.iota('int32', n)

    if dtypes.issubdtype(a.dtype, np.complexfloating):
      t = a[:, k]
      magnitude = abs(t.real) + abs(t.imag)
    else:
      magnitude = abs(a[:, k])
    i = lax.argmax(lax.select(m_idx >= k, magnitude, lax.full_like(magnitude, -np.inf)),
                   axis=0, index_dtype=pivot.dtype)
    pivot = pivot.at[k].set(i)
    a = a.at[[k, i],].set(a[[i, k],])
    perm = perm.at[[i, k],].set(perm[[k, i],])

    # a[k+1:, k] /= a[k, k], adapted for loop-invariant shapes
    x = a[k, k]
    a = a.at[:, k].set(lax.select((m_idx > k) & (x != 0), a[:, k] / x, a[:, k]))

    # a[k+1:, k+1:] -= jnp.outer(a[k+1:, k], a[k, k+1:])
    a_outer = a[:, k, None] * a[k, None]
    a = a - lax.select((m_idx[:, None] > k) & (n_idx[None, :] > k),
                       a_outer, lax._zeros(a_outer))
    return pivot, perm, a

  pivot = lax.full((min(m, n),), 0, dtype=np.int32)
  perm = lax.iota('int32', m)
  if m == 0 and n == 0:
    # If the array is empty, the loop body never executes but tracing it to a
    # jaxpr fails because the indexing cannot succeed.
    return (pivot, perm, a)
  return control_flow.fori_loop(0, min(m, n), body, (pivot, perm, a))

