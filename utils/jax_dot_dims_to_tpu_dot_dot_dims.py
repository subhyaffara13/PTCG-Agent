
def jax_dot_dims_to_tpu_dot_dot_dims(
    dimension_numbers,
    lhs_shape,
    rhs_shape,
    excluding_lhs_dims=frozenset(),
    excluding_rhs_dims=frozenset(),
):
  """Converts a jax dot dimension numbers to a tpu dot dimension numbers.

  Jax dot dimension numbers are given as a tuple of tuples of sequences of ints
  of the form ((lhs_contracting_dims, rhs_contracting_dims), (lhs_batch_dims,
  rhs_batch_dims)).

  TPU dot dimension numbers are given as an MLIR definition of the form
  #tpu.dot_dimension_numbers - which can be found in the tpu dilect definition
  # file, tpu.td .

  Args:
    dimension_numbers: The jax dot dimension numbers.
    lhs_shape: The shape of the left hand side.
    rhs_shape: The shape of the right hand side.
    excluding_lhs_dims: The dimensions of the left hand side to exclude. If
      specified, these dimensions won't be included in the dot dimension
      numbers. It's useful when dimensions are not used in contracting, batch,
      or non-contracting.
    excluding_rhs_dims: Same as `excluding_lhs_dims`, but for the right hand
      side.

  Returns:
    The tpu dot dimension numbers.
  """
  (contracting_dims, batch_dims) = dimension_numbers
  lhs_contracting_dims, rhs_contracting_dims = contracting_dims
  lhs_batch_dims, rhs_batch_dims = batch_dims

  lhs_total_dims = set(range(len(lhs_shape))) - excluding_lhs_dims
  rhs_total_dims = set(range(len(rhs_shape))) - excluding_rhs_dims

  lhs_non_contracting_dims = sorted(
      lhs_total_dims - set(lhs_contracting_dims) - set(lhs_batch_dims)
  )
  rhs_non_contracting_dims = sorted(
      rhs_total_dims - set(rhs_contracting_dims) - set(rhs_batch_dims)
  )

  # Create output_dim_order
  # Note: we assume that the output dimensions are ordered as batch dims, lhs_non_contracting_dims,
  # rhs_non_contracting_dims - this assumption is safe to make, as it is
  # the same one made in jax's dot_general.
  output_dim_order = []

  lhs_dim_map = {dim: idx for idx, dim in enumerate(range(len(lhs_shape)))}
  rhs_dim_map = {dim: idx for idx, dim in enumerate(range(len(rhs_shape)))}

  for dim in lhs_batch_dims:
    output_dim_order.append(0)
    output_dim_order.append(lhs_dim_map[dim])

  for dim in lhs_non_contracting_dims:
    output_dim_order.append(0)
    output_dim_order.append(lhs_dim_map[dim])

  for dim in rhs_non_contracting_dims:
    output_dim_order.append(1)
    output_dim_order.append(rhs_dim_map[dim])

  def format_dims(dims):
    return "[" + ", ".join(str(d) for d in dims) + "]"

  all_dims = (
      lhs_contracting_dims,
      rhs_contracting_dims,
      lhs_non_contracting_dims,
      rhs_non_contracting_dims,
      output_dim_order,
      lhs_batch_dims,
      rhs_batch_dims,
  )
  tpu_dim_numbers_str = (
      f"#tpu.dot_dimension_numbers<{','.join(map(format_dims, all_dims))}>"
  )

  return ir.Attribute.parse(tpu_dim_numbers_str)

