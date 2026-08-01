
def lpmn(m: int, n: int, z: Array) -> tuple[Array, Array]:
  """The associated Legendre functions (ALFs) of the first kind.

  Args:
    m: The maximum order of the associated Legendre functions.
    n: The maximum degree of the associated Legendre function, often called
      `l` in describing ALFs. Both the degrees and orders are
      `[0, 1, 2, ..., l_max]`, where `l_max` denotes the maximum degree.
    z: A vector of type `float32` or `float64` containing the sampling
      points at which the ALFs are computed.

  Returns:
    A 2-tuple of 3D arrays of shape `(l_max + 1, l_max + 1, len(z))` containing
    the values and derivatives of the associated Legendre functions of the
    first kind. The return type matches the type of `z`.

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
  is_normalized = False
  p_vals = _gen_associated_legendre(l_max, z, is_normalized)
  p_derivatives = _gen_derivatives(p_vals, z, is_normalized)

  return (p_vals, p_derivatives)

