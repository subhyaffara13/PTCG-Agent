
def bcsr_extract(indices: ArrayLike, indptr: ArrayLike, mat: ArrayLike) -> Array:
  """Extract values from a dense matrix at given BCSR (indices, indptr).

  Args:
    indices: An ndarray; see BCSR indices.
    indptr: An ndarray; see BCSR indptr.
    mat: A dense matrix.

  Returns:
    An ndarray; see BCSR data.
  """
  return bcsr_extract_p.bind(indices, indptr, mat)

