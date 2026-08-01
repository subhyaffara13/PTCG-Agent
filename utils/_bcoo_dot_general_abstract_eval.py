
def _bcoo_dot_general_abstract_eval(lhs_data, lhs_indices, rhs, *, dimension_numbers,
                                    preferred_element_type, lhs_spinfo: SparseInfo):
  out_aval = jax.jit(lax.dot_general, static_argnames=("dimension_numbers", "preferred_element_type")).eval_shape(
          jax.ShapeDtypeStruct(lhs_spinfo.shape, lhs_data.dtype),
          jax.ShapeDtypeStruct(rhs.shape, rhs.dtype),
          dimension_numbers=dimension_numbers,
          preferred_element_type=preferred_element_type)

  (lhs_contracting, _), (lhs_batch, _) = dimension_numbers
  n_batch, n_sparse, _, _ = _validate_bcoo(lhs_data, lhs_indices, lhs_spinfo.shape)
  if lhs_batch and max(lhs_batch) >= n_batch:
    raise NotImplementedError(
      "bcoo_dot_general batch dimensions must be among the batch dimensions in the sparse representation.\n"
      f"got {lhs_batch=}, {n_batch=}")

  # TODO: support contraction of dense dimensions?
  if any(d >= n_batch + n_sparse for d in lhs_contracting):
    raise NotImplementedError("bcoo_dot_general: contracting over dense dimensions.")

  return core.ShapedArray(out_aval.shape, out_aval.dtype)

