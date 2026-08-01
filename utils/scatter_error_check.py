
def scatter_error_check(prim, error, enabled_errors, operand, indices, updates,
                        *, update_jaxpr, update_consts, dimension_numbers,
                        indices_are_sorted, unique_indices, mode):
  """Checks if indices are within bounds and update does not generate NaN."""
  out = prim.bind(
      operand, indices, updates, update_jaxpr=update_jaxpr,
      update_consts=update_consts, dimension_numbers=dimension_numbers,
      indices_are_sorted=indices_are_sorted, unique_indices=unique_indices,
      mode=mode)

  if OOBError not in enabled_errors:
    return error, out

  out_of_bounds, payload = scatter_oob(operand, indices, updates, dimension_numbers)
  oob_error = OOBError(get_traceback(), prim.name, operand.shape, payload)
  error = assert_func(error, out_of_bounds, oob_error)
  error = check_nans(prim, error, enabled_errors, out)
  return error, out

