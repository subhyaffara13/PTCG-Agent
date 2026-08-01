
def sph_harm_y(n: Array,
               m: Array,
               theta: Array,
               phi: Array,
               diff_n: int | None = None,
               n_max: int | None = None) -> Array:
  r"""Computes the spherical harmonics.

  The JAX version has one extra argument `n_max`, the maximum value in `n`.

  The spherical harmonic of degree `n` and order `m` can be written as
  :math:`Y_n^m(\theta, \phi) = N_n^m * P_n^m(\cos \theta) * \exp(i m \phi)`,
  where :math:`N_n^m = \sqrt{\frac{\left(2n+1\right) \left(n-m\right)!}
  {4 \pi \left(n+m\right)!}}` is the normalization factor and :math:`\theta` and
  :math:`\phi` are the colatitude and longitude, respectively. :math:`N_n^m` is
  chosen in the way that the spherical harmonics form a set of orthonormal basis
  functions of :math:`L^2(S^2)`.

  Args:
    n: The degree of the harmonic; must have `n >= 0`. The standard notation for
      degree in descriptions of spherical harmonics is `l (lower case L)`. We
      use `n` here to be consistent with `scipy.special.sph_harm_y`. Return
      values for `n < 0` are undefined.
    m: The order of the harmonic; must have `|m| <= n`. Return values for
      `|m| > n` are undefined.
    theta: The polar (colatitudinal) coordinate; must be in [0, pi].
    phi: The azimuthal (longitudinal) coordinate; must be in [0, 2*pi].
    diff_n: Unsupported by JAX.
    n_max: The maximum degree `max(n)`. If the supplied `n_max` is not the true
      maximum value of `n`, the results are clipped to `n_max`. For example,
      `sph_harm(m=jnp.array([2]), n=jnp.array([10]), theta, phi, n_max=6)`
      actually returns
      `sph_harm(m=jnp.array([2]), n=jnp.array([6]), theta, phi, n_max=6)`
  Returns:
    A 1D array containing the spherical harmonics at (m, n, theta, phi).
  """
  if diff_n is not None:
    raise NotImplementedError(
        "The 'diff_n' argument to jax.scipy.special.sph_harm_y is not supported.")

  if jnp.isscalar(theta):
    theta = jnp.array([theta])

  if n_max is None:
    n_max = np.max(n)
  n_max = core.concrete_or_error(
      int, n_max, 'The `n_max` argument of `jnp.scipy.special.sph_harm` must '
      'be statically specified to use `sph_harm` within JAX transformations.')

  return _sph_harm(n, m, theta, phi, n_max)

