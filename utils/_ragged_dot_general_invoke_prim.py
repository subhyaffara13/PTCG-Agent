
def _ragged_dot_general_invoke_prim(
    group_sizes,
    lhs,
    rhs,
    new_ragged_dot_dimension_numbers,
    precision,
    preferred_element_type,
    out_sharding,
):
  del out_sharding
  return ragged_dot_general(
      lhs,
      rhs,
      group_sizes,
      ragged_dot_dimension_numbers=new_ragged_dot_dimension_numbers,
      precision=precision,
      preferred_element_type=preferred_element_type,
  )

