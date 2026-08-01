
def lpmn_values(m: int, n: int, z: Array, is_normalized: bool) -> Array:
  r"""The associated Legendre functions (ALFs) of the first kind.

  Unlike `lpmn`, this function only computes the values of ALFs.
  The ALFs of the first kind can be used in spherical harmonics. The
  spherical harmonic of degree `l` and order `m` can be written as
  :math:`Y_l^m(\theta, \phi) = N_l^m * P_l^m(\cos \theta) * \exp(i m \phi)`,
  where :math:`N_l^m` is the normalization factor and θ and φ are the
  colatitude and longitude, respectively. :math:`N_l^m` is chosen in the
  way that the spherical harmonics form a set of orthonormal basis function
  of :math:`L^2(S^2)`. Normalizing :math:`P_l^m` avoids overflow/underflow
  and achieves better numerical stability.

  Args:
    m: The maximum order of the associated Legendre functions.
    n: The maximum degree of the associated Legendre function, often called
      `l` in describing ALFs. Both the degrees and orders are
      `[0, 1, 2, ..., l_max]`, where `l_max` denotes the maximum degree.
    z: A vector of type `float32` or `float64` containing the sampling
      points at which the ALFs are computed.
    is_normalized: True if the associated Legendre functions are normalized.
      With normalization, :math:`N_l^m` is applied such that the spherical
      harmonics form a set of orthonormal basis functions of :math:`L^2(S^2)`.

  Returns:
    A 3D array of shape `(l_max + 1, l_max + 1, len(z))` containing
    the values of the associated Legendre functions of the first kind. The
    return type matches the type of `z`.

  Raises:
    TypeError if elements of array `z` are not in (float32, float64).
    ValueError if array `z` is not 1D.
    NotImplementedError if `m!=n`.
  """
  dtype = lax.dtype(z)
  if dtype not in (np.float32, np.float64):
    raise TypeError(
        'z.dtype={} is not supported, see docstring for supported types.'
        .format(dtype))

  if z.ndim != 1:
    raise ValueError('z must be a 1D array.')

  m = core.concrete_or_error(int, m, 'Argument m of lpmn.')
  n = core.concrete_or_error(int, n, 'Argument n of lpmn.')

  if m != n:
    raise NotImplementedError('Computations for m!=n are not yet supported.')

  l_max = n

  return _gen_associated_legendre(l_max, z, is_normalized)

