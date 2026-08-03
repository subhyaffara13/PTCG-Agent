import re

def _eigh_qdwh_impl(x, *, lower, sort_eigenvalues, subset_by_index):
  """QDWH-based eigendecomposition for TPU."""
  *_, m, n = x.shape
  assert m == n, (m, n)

  termination_size = 256
  if not core.is_constant_dim(m):
    # TODO: maybe we can relax the check below for shape polymorphism?
    raise NotImplementedError(
        "Shape polymorphism for native lowering for eigh is implemented "
        f"only for the batch dimensions: {x.shape}")

  if m <= termination_size and (
      subset_by_index is None or subset_by_index == (0, n)
  ):
    return lax_linalg.eigh(
        x, lower=lower, sort_eigenvalues=sort_eigenvalues,
        symmetrize_input=False,
        implementation=lax_linalg.EighImplementation.JACOBI
    )

  def eigh_qdwh(x):
    if len(x.shape) > 2:
      return control_flow.map(eigh_qdwh, x)

    # We should only look at elements from the lower/upper triangle. Reflects
    # that triangle into the other triangle to form a Hermitian matrix.
    if lower:
      mask = lax_internal._tri(bool, (n, n), 0)
    else:
      mask = lax.bitwise_not(lax_internal._tri(bool, (n, n), -1))
    if dtypes.issubdtype(x.dtype, np.complexfloating):
      re = lax.select(mask, lax.real(x), _T(lax.real(x)))
      if lower:
        im_mask = lax_internal._tri(bool, (n, n), -1)
      else:
        im_mask = lax.bitwise_not(lax_internal._tri(bool, (n, n), 0))
      im = lax.imag(x)
      im = lax.select(im_mask, im, lax.full_like(im, 0))
      im = lax.select(mask, im, -_T(im))
      x = lax.complex(re, im)
    else:
      x = lax.select(mask, x, _T(x))

    return eigh(
        x,
        sort_eigenvalues=sort_eigenvalues,
        termination_size=termination_size,
        subset_by_index=subset_by_index,
    )

  eig_vals, eig_vecs = eigh_qdwh(x)
  return eig_vecs, eig_vals

