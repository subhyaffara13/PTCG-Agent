
def _schur_dtype_rule(dtype, *, compute_schur_vectors, **_):
  return (dtype, dtype) if compute_schur_vectors else (dtype,)

