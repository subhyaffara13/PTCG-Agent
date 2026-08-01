
def _eig_dtype_rule(
    a_dtype, *, compute_left_eigenvectors, compute_right_eigenvectors, **_
):
  dtype = dtypes.to_complex_dtype(a_dtype)
  return (dtype,) * (1 + compute_left_eigenvectors + compute_right_eigenvectors)

