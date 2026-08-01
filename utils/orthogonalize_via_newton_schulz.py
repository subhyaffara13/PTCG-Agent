
def orthogonalize_via_newton_schulz(
    x: jax.Array,
    ns_coeffs: jax.Array,
    ns_steps: jax.typing.ArrayLike = 5,
    preconditioning: Literal[
        'frobenius', 'spectral', 'aol', 'schatten'
    ] = 'frobenius',
    eps: jax.typing.ArrayLike = 1e-8,
    dimension_numbers: MuonDimensionNumbers | None = None,
) -> jax.Array:
  r"""Orthogonalize via Newton-Schulz iteration.

  We opt to use a quintic iteration whose coefficients are selected to maximize
  the slope at zero. For the purpose of minimizing steps, it turns out to be
  empirically effective to keep increasing the slope at zero even beyond the
  point where the iteration no longer converges all the way to one everywhere
  on the interval. This iteration therefore does not produce UV^T but rather
  something like US'V^T where S' is diagonal with S_{ii}' ~ Uniform(0.5, 1.5),
  which turns out not to hurt model performance at all relative to UV^T, where
  USV^T = G is the SVD.

  Args:
    x: A matrix to orthogonalize.
    ns_coeffs: Coefficients for the Newton-schulz iterators.
      Must have shape (n, 3) where n is the number of iterations.
    ns_steps: Number of Newton-schulz iterations.
      Ignored if `ns_coeffs` is a 2D array.
    preconditioning: Which preconditioning method to use.
    eps: Term added to denominators to improve numerical stability.
    dimension_numbers: Optional spec for reshaping a tensor before and after the
      orthogonalization, to support non-2D parameters.

  Returns:
    The orthogonalized matrix.
  """
  if x.ndim != 2 and not isinstance(dimension_numbers, MuonDimensionNumbers):
    raise ValueError(
        f'Input must have shape (m, n) or weight dimension numbers must be'
        f' provided. Got shape={x.shape} and {dimension_numbers=}.')
  if x.ndim == 2:
    dimension_numbers = MuonDimensionNumbers(reduction_axis=0, output_axis=1)
  if ns_coeffs.ndim > 2 or ns_coeffs.shape[-1] != 3:
    raise ValueError('Newton-Schulz coefficients must have shape (3,) or'
                     f' (n, 3), got {ns_coeffs.shape}')

  def _orthogonalize(x):
    transposed = False
    if x.shape[0] > x.shape[1]:
      x = x.T
      transposed = True

    ns_iterators = {
        'frobenius': _base_ns_iterator,
        'spectral': _base_ns_iterator,
        'aol': _aol_ns_iterator,
        'schatten': _schatten_ns_iterator,
    }
    if preconditioning not in _PRECONDITIONINGS:
      raise ValueError(f'Unknown preconditioning {preconditioning}')
    _ns_iterator = ns_iterators[preconditioning]

    if preconditioning == 'frobenius':
      x /= jnp.linalg.norm(x, ord='fro') + eps
    elif preconditioning == 'spectral':
      x /= jnp.linalg.norm(x, ord=2) + eps
    else:
      pass

    ns_coeffs_ = ns_coeffs.astype(x.dtype)

    if ns_coeffs_.ndim == 1:
      x = jax.lax.fori_loop(
          0, ns_steps, lambda i, x: _ns_iterator(i, x, ns_coeffs_), x,
          unroll=True)  # Unroll to ensure efficient composition with jax.vmap.
    else:
      def _scan_body(carry, coeffs_step):
        i, x = carry
        x_new = _ns_iterator(i, x, coeffs_step)
        return (i + 1, x_new), None

      init_carry = (jnp.asarray(0, dtype=jnp.int32), x)
      (_, x), _ = jax.lax.scan(_scan_body, init_carry, ns_coeffs_)

    if transposed:
      x = x.T
    return x

  reshape_fn, inverse_fn = _compute_muon_reshape(x, dimension_numbers)
  return inverse_fn(jax.vmap(_orthogonalize)(reshape_fn(x)))

