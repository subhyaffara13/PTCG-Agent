
def _gather_sparse_rule(spenv, *args, dimension_numbers, slice_sizes, unique_indices,
                        indices_are_sorted, mode, fill_value):
  operand, start_indices = spvalues_to_arrays(spenv, args)
  result = sparse.bcoo_gather(operand, start_indices, dimension_numbers=dimension_numbers,
                              slice_sizes=slice_sizes, unique_indices=unique_indices,
                              indices_are_sorted=indices_are_sorted,
                              mode=mode, fill_value=fill_value)
  return arrays_to_spvalues(spenv, (result,))

