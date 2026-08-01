
def compute_dot_output_shape(
    lhs_shape, rhs_shape, lhs_dimension_numbers, rhs_dimension_numbers
  ):
  """
  Computes the output shape for a `lax.dot_general`-like operation.
  """
  lhs_contract, lhs_batch = lhs_dimension_numbers[0], lhs_dimension_numbers[1]
  rhs_contract, rhs_batch = rhs_dimension_numbers[0], rhs_dimension_numbers[1]

  output_shape = []
  # Add dimensions for batch (assuming the batch dims of LHS and RHS
  # should be same)
  for i, dim in enumerate(lhs_shape):
    if i in lhs_batch:
      output_shape.append(dim)
  # Add dimensions from the LHS that are non contracting
  for i, dim in enumerate(lhs_shape):
    if i not in lhs_contract and i not in lhs_batch:
      output_shape.append(dim)
  # Add dimensions from the RHS that are non contracting
  for i, dim in enumerate(rhs_shape):
    if i not in rhs_contract and i not in rhs_batch:
      output_shape.append(dim)
  return tuple(output_shape)

