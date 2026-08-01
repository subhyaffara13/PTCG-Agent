
def _gen_recurrence_mask(
    l_max: int, is_normalized: bool, dtype: Any
) -> tuple[Array, Array]:
  """Generates a mask for recurrence relation on the remaining entries.

  The remaining entries are with respect to the diagonal and offdiagonal
  entries.

  Args:
    l_max: see `gen_normalized_legendre`.
    is_normalized: True if the recurrence mask is used by normalized associated
      Legendre functions.

  Returns:
    Arrays representing the mask used by the recurrence relations.
  """

  # Computes all coefficients.
  m_mat, l_mat = jnp.meshgrid(
    jnp.arange(l_max + 1, dtype=dtype),
    jnp.arange(l_max + 1, dtype=dtype),
    indexing='ij')
  if is_normalized:
    c0 = l_mat * l_mat
    c1 = m_mat * m_mat
    c2 = 2.0 * l_mat
    c3 = (l_mat - 1.0) * (l_mat - 1.0)
    d0 = jnp.sqrt((4.0 * c0 - 1.0) / (c0 - c1))
    d1 = jnp.sqrt(((c2 + 1.0) * (c3 - c1)) / ((c2 - 3.0) * (c0 - c1)))
  else:
    d0 = (2.0 * l_mat - 1.0) / (l_mat - m_mat)
    d1 = (l_mat + m_mat - 1.0) / (l_mat - m_mat)

  d0_mask_indices = jnp.triu_indices(l_max + 1, 1)
  d1_mask_indices = jnp.triu_indices(l_max + 1, 2)
  d_zeros = jnp.zeros((l_max + 1, l_max + 1), dtype=dtype)
  d0_mask = d_zeros.at[d0_mask_indices].set(d0[d0_mask_indices])
  d1_mask = d_zeros.at[d1_mask_indices].set(d1[d1_mask_indices])

  # Creates a 3D mask that contains 1s on the diagonal plane and 0s elsewhere.
  # i = jnp.arange(l_max + 1)[:, None, None]
  # j = jnp.arange(l_max + 1)[None, :, None]
  # k = jnp.arange(l_max + 1)[None, None, :]
  i, j, k = jnp.ogrid[:l_max + 1, :l_max + 1, :l_max + 1]
  mask = (i + j - k == 0).astype(dtype)

  d0_mask_3d = jnp_einsum.einsum('jk,ijk->ijk', d0_mask, mask)
  d1_mask_3d = jnp_einsum.einsum('jk,ijk->ijk', d1_mask, mask)

  return (d0_mask_3d, d1_mask_3d)

