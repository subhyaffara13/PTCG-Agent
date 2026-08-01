
def _gather_jvp_rule(g, operand, indices, *, dimension_numbers,
                     slice_sizes, unique_indices, indices_are_sorted, mode,
                     fill_value):
  return gather(g, indices, dimension_numbers, slice_sizes,
                unique_indices=unique_indices,
                indices_are_sorted=indices_are_sorted, mode=mode,
                fill_value=0)

