
def gather_error_check(error, enabled_errors, operand, start_indices, *,
                       dimension_numbers, slice_sizes, unique_indices,
                       indices_are_sorted, mode, fill_value):
  out = lax.gather_p.bind(
      operand, start_indices, dimension_numbers=dimension_numbers,
      slice_sizes=slice_sizes, unique_indices=unique_indices,
      indices_are_sorted=indices_are_sorted, mode=mode, fill_value=fill_value)

  if OOBError not in enabled_errors:
    return error, out

  # compare to OOB masking logic in lax._gather_translation_rule
  dnums = dimension_numbers
  operand_dims = np.array(operand.shape)
  num_batch_dims = len(start_indices.shape) - 1

  upper_bound = operand_dims[np.array(dnums.start_index_map)]
  upper_bound -= np.array(slice_sizes)[np.array(dnums.start_index_map)]
  upper_bound = jnp.expand_dims(upper_bound, axis=tuple(range(num_batch_dims)))
  oob_mask = (start_indices < 0) | (start_indices > upper_bound.astype(start_indices.dtype))

  payload = oob_payload(oob_mask, start_indices, dnums.start_index_map, operand.shape)
  error = assert_func(error, jnp.any(oob_mask), OOBError(get_traceback(), "gather", operand.shape, payload))
  return error, out

