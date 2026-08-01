
def _bcoo_dot_general_sampled_impl(A, B, indices, *, dimension_numbers):
  A = jnp.asarray(A)
  B = jnp.asarray(B)
  indices = jnp.asarray(indices)
  (lhs_contract, rhs_contract), (lhs_batch, rhs_batch) = dimension_numbers
  n_batch = indices.ndim - 2
  n_sparse = indices.shape[-1]
  precision = lax.Precision.HIGHEST

  # TODO(jakevdp): add fast approach for more general cases / combine the following:
  if (not (lhs_contract or rhs_contract or lhs_batch or rhs_batch)
      and A.ndim == B.ndim == 1 and n_sparse + n_batch == 2):
    return _bcoo_dot_general_sampled_simple(A, B, indices, dimension_numbers=dimension_numbers, precision=precision)
  if len(lhs_contract) == 1 and not lhs_batch and A.ndim == B.ndim == 2 and n_sparse + n_batch == 2:
    return _bcoo_dot_general_sampled_simple2(A, B, indices, dimension_numbers=dimension_numbers, precision=precision)


  return _bcoo_dot_general_sampled_slow(A, B, indices, dimension_numbers=dimension_numbers, precision=precision)

