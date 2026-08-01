
def _bcsr_dot_general_abstract_eval(lhs_data, lhs_indices, lhs_indptr, rhs, *,
                                    dimension_numbers, preferred_element_type, lhs_spinfo):
  (lhs_contracting, _), (lhs_batch, _) = dimension_numbers
  props = _validate_bcsr_indices(lhs_indices, lhs_indptr, lhs_spinfo.shape)
  out_aval = jax.eval_shape(
    partial(lax.dot_general,
            dimension_numbers=dimension_numbers,
            preferred_element_type=preferred_element_type),
    jax.ShapeDtypeStruct(lhs_spinfo.shape, lhs_data.dtype),
    jax.ShapeDtypeStruct(rhs.shape, rhs.dtype))

  if lhs_batch and max(lhs_batch) >= props.n_batch:
    raise NotImplementedError(
      "bcsr_dot_general batch dimensions must be among the batch dimensions in the sparse representtaion.\n"
      f"got {lhs_batch=}, {props.n_batch=}")

  # TODO: support contraction of dense dimensions?
  if any(d >= props.n_batch + 2 for d in lhs_contracting):
    raise NotImplementedError("bcsr_dot_general: contracting over dense dimensions.")

  return core.ShapedArray(out_aval.shape, out_aval.dtype)

