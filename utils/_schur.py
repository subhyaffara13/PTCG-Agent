
def _schur(a: Array, output: str) -> tuple[Array, Array]:
  if output == "complex":
    a = a.astype(dtypes.to_complex_dtype(a.dtype))
  return lax_linalg.schur(a)

