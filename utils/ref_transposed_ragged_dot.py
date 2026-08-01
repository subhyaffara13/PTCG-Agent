
def ref_transposed_ragged_dot(lhs, rhs, group_sizes):
  return jax.lax.ragged_dot_general(
      lhs, rhs, group_sizes,
      ragged_dot_dimension_numbers=jax.lax.RaggedDotDimensionNumbers(
          dot_dimension_numbers=(((0,), (0,)), ((), ())),
          lhs_ragged_dimensions=[0],
          rhs_group_dimensions=[],
      )
  )

