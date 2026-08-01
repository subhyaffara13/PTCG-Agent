
def _gen_associated_legendre(l_max: int,
                             x: Array,
                             is_normalized: bool) -> Array:
  r"""Computes associated Legendre functions (ALFs) of the first kind.

  The ALFs of the first kind are used in spherical harmonics. The spherical
  harmonic of degree `l` and order `m` can be written as
  `Y_l^m(θ, φ) = N_l^m * P_l^m(cos(θ)) * exp(i m φ)`, where `N_l^m` is the
  normalization factor and θ and φ are the colatitude and longitude,
  respectively. `N_l^m` is chosen in the way that the spherical harmonics form
  a set of orthonormal basis functions of L^2(S^2). For the computational
  efficiency of spherical harmonics transform, the normalization factor is
  used in the computation of the ALFs. In addition, normalizing `P_l^m`
  avoids overflow/underflow and achieves better numerical stability. Three
  recurrence relations are used in the computation.

  Args:
    l_max: The maximum degree of the associated Legendre function. Both the
      degrees and orders are `[0, 1, 2, ..., l_max]`.
    x: A vector of type `float32`, `float64` containing the sampled points in
      spherical coordinates, at which the ALFs are computed; `x` is essentially
      `cos(θ)`. For the numerical integration used by the spherical harmonics
      transforms, `x` contains the quadrature points in the interval of
      `[-1, 1]`. There are several approaches to provide the quadrature points:
      Gauss-Legendre method (`scipy.special.roots_legendre`), Gauss-Chebyshev
      method (`scipy.special.roots_chebyu`), and Driscoll & Healy
      method (Driscoll, James R., and Dennis M. Healy. "Computing Fourier
      transforms and convolutions on the 2-sphere." Advances in applied
      mathematics 15, no. 2 (1994): 202-250.). The Gauss-Legendre quadrature
      points are nearly equal-spaced along θ and provide exact discrete
      orthogonality, (P^m)^T W P_m = I, where `T` represents the transpose
      operation, `W` is a diagonal matrix containing the quadrature weights,
      and `I` is the identity matrix. The Gauss-Chebyshev points are equally
      spaced, which only provide approximate discrete orthogonality. The
      Driscoll & Healy quadrature points are equally spaced and provide the
      exact discrete orthogonality. The number of sampling points is required to
      be twice as the number of frequency points (modes) in the Driscoll & Healy
      approach, which enables FFT and achieves a fast spherical harmonics
      transform.
    is_normalized: True if the associated Legendre functions are normalized.
      With normalization, `N_l^m` is applied such that the spherical harmonics
      form a set of orthonormal basis functions of L^2(S^2).

  Returns:
    The 3D array of shape `(l_max + 1, l_max + 1, len(x))` containing the values
    of the ALFs at `x`; the dimensions in the sequence of order, degree, and
    evaluation points.
  """
  p = jnp.zeros((l_max + 1, l_max + 1, x.shape[0]), dtype=x.dtype)

  a_idx = jnp.arange(1, l_max + 1, dtype=x.dtype)
  b_idx = jnp.arange(l_max, dtype=x.dtype)
  if is_normalized:
    initial_value: ArrayLike = 0.5 / jnp.sqrt(np.pi)  # The initial value p(0,0).
    f_a = jnp.cumprod(-1 * jnp.sqrt(1.0 + 0.5 / a_idx))
    f_b = jnp.sqrt(2.0 * b_idx + 3.0)
  else:
    initial_value = 1.0  # The initial value p(0,0).
    f_a = jnp.cumprod(1.0 - 2.0 * a_idx)
    f_b = 2.0 * b_idx + 1.0

  p = p.at[(0, 0)].set(initial_value)

  # Compute the diagonal entries p(l,l) with recurrence.
  y = jnp.cumprod(
      jnp.broadcast_to(jnp.sqrt(1.0 - x * x), (l_max, x.shape[0])),
      axis=0)
  p_diag = initial_value * jnp_einsum.einsum('i,ij->ij', f_a, y)
  diag_indices = jnp.diag_indices(l_max + 1)
  p = p.at[(diag_indices[0][1:], diag_indices[1][1:])].set(p_diag)

  # Compute the off-diagonal entries with recurrence.
  p_offdiag = jnp_einsum.einsum('ij,ij->ij',
                         jnp_einsum.einsum('i,j->ij', f_b, x),
                         p[jnp.diag_indices(l_max)])
  offdiag_indices = (diag_indices[0][:l_max], diag_indices[1][:l_max] + 1)
  p = p.at[offdiag_indices].set(p_offdiag)

  # Compute the remaining entries with recurrence.
  d0_mask_3d, d1_mask_3d = _gen_recurrence_mask(
      l_max, is_normalized=is_normalized, dtype=x.dtype)

  def body_fun(i, p_val):
    coeff_0 = d0_mask_3d[i]
    coeff_1 = d1_mask_3d[i]
    h = (jnp_einsum.einsum('ij,ijk->ijk',
                    coeff_0,
                    jnp_einsum.einsum(
                        'ijk,k->ijk', jnp.roll(p_val, shift=1, axis=1), x)) -
         jnp_einsum.einsum('ij,ijk->ijk', coeff_1, jnp.roll(p_val, shift=2, axis=1)))
    p_val = p_val + h
    return p_val

  # TODO(jakevdp): use some sort of fixed-point procedure here instead?
  p = p.astype(dtypes.result_type(p, x, d0_mask_3d))
  if l_max > 1:
    p = lax.fori_loop(lower=2, upper=l_max+1, body_fun=body_fun, init_val=p)

  return p

