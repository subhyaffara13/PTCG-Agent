
def _bcoo_dot_general_sampled_jvp_B(B_dot, A, B, indices, *, dimension_numbers):
  return bcoo_dot_general_sampled(A, B_dot, indices, dimension_numbers=dimension_numbers)

