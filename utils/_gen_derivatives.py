
def _gen_derivatives(p: Array,
                     x: Array,
                     is_normalized: bool) -> Array:
  """Generates derivatives of associated Legendre functions of the first kind.

  Args:
    p: The 3D array containing the values of associated Legendre functions; the
      dimensions are in the sequence of order (m), degree (l), and evaluation
      points.
    x: A vector of type `float32` or `float64` containing the sampled points.
    is_normalized: True if the associated Legendre functions are normalized.
  Returns:
    The 3D array representing the derivatives of associated Legendre functions
    of the first kind.
  """

  num_m, num_l, num_x = p.shape

  # p_{l-1}^m.
  p_m_lm1 = jnp.pad(p, ((0, 0), (1, 0), (0, 0)))[:, :num_l, :]

  # p_{l-1}^{m+2}.
  p_mp2_lm1 = jnp.pad(p_m_lm1, ((0, 2), (0, 0), (0, 0)))[2:num_m + 2, :, :]

  # p_{l-1}^{m-2}.
  p_mm2_lm1 = jnp.pad(p_m_lm1, ((2, 0), (0, 0), (0, 0)))[:num_m, :, :]

  # Derivative computation requires negative orders.
  if is_normalized:
    raise NotImplementedError(
        'Negative orders for normalization is not implemented yet.')
  else:
    if num_l > 1:
      l_vec = jnp.arange(1, num_l - 1, dtype=x.dtype)
      p_p1 = p[1, 1:num_l - 1, :]
      coeff = -1.0 / ((l_vec + 1) * l_vec)
      update_p_p1 = jnp_einsum.einsum('i,ij->ij', coeff, p_p1)
      p_mm2_lm1 = p_mm2_lm1.at[1, 2:num_l, :].set(update_p_p1)

    if num_l > 2:
      l_vec = jnp.arange(2, num_l - 1, dtype=x.dtype)
      p_p2 = p[2, 2:num_l - 1, :]
      coeff = 1.0 / ((l_vec + 2) * (l_vec + 1) * l_vec * (l_vec - 1))
      update_p_p2 = jnp_einsum.einsum('i,ij->ij', coeff, p_p2)
      p_mm2_lm1 = p_mm2_lm1.at[0, 3:num_l, :].set(update_p_p2)

  m_mat, l_mat = jnp.meshgrid(
    jnp.arange(num_m, dtype=x.dtype),
    jnp.arange(num_l, dtype=x.dtype),
    indexing='ij')

  coeff_zeros = jnp.zeros((num_m, num_l), dtype=x.dtype)
  upper_0_indices = jnp.triu_indices(num_m, 0, num_l)
  zero_vec = jnp.zeros((num_l,), dtype=x.dtype)

  a0 = -0.5 / (m_mat - 1.0)
  a0_masked = coeff_zeros.at[upper_0_indices].set(a0[upper_0_indices])
  a0_masked = a0_masked.at[1, :].set(zero_vec)

  b0 = l_mat + m_mat
  c0 = a0 * (b0 - 2.0) * (b0 - 1.0)
  c0_masked = coeff_zeros.at[upper_0_indices].set(c0[upper_0_indices])
  c0_masked = c0_masked.at[1, :].set(zero_vec)

  # p_l^{m-1}.
  p_mm1_l = (jnp_einsum.einsum('ij,ijk->ijk', a0_masked, p_m_lm1) +
             jnp_einsum.einsum('ij,ijk->ijk', c0_masked, p_mm2_lm1))

  d0 = -0.5 / (m_mat + 1.0)
  d0_masked = coeff_zeros.at[upper_0_indices].set(d0[upper_0_indices])
  e0 = d0 * b0 * (b0 + 1.0)
  e0_masked = coeff_zeros.at[upper_0_indices].set(e0[upper_0_indices])

  # p_l^{m+1}.
  p_mp1_l = (jnp_einsum.einsum('ij,ijk->ijk', d0_masked, p_mp2_lm1) +
             jnp_einsum.einsum('ij,ijk->ijk', e0_masked, p_m_lm1))

  f0 = b0 * (l_mat - m_mat + 1.0) / 2.0
  f0_masked = coeff_zeros.at[upper_0_indices].set(f0[upper_0_indices])
  p_derivative = jnp_einsum.einsum('ij,ijk->ijk', f0_masked, p_mm1_l) - 0.5 * p_mp1_l

  # Special treatment of the singularity at m = 1.
  if num_m > 1:
    l_vec = jnp.arange(num_l, dtype=p.dtype)
    g0 = jnp_einsum.einsum('i,ij->ij', (l_vec + 1) * l_vec, p[0, :, :])
    if num_l > 2:
      g0 = g0 -  p[2, :, :]
    p_derivative_m0 = jnp_einsum.einsum('j,ij->ij', 0.5 / jnp.sqrt(1 - x * x), g0)
    p_derivative = p_derivative.at[1, :, :].set(p_derivative_m0)
    p_derivative = p_derivative.at[1, 0, :].set(0)

  return p_derivative

