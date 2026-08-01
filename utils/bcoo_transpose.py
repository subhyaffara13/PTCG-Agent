
def bcoo_transpose(mat: BCOO, *, permutation: Sequence[int]) -> BCOO:
  """Transpose a BCOO-format array.

  Args:
    mat: A BCOO-format array.
    permutation:  A tuple or list or ndarray which contains a permutation of
      [0,1,..,N-1] where N is the number of axes of ``mat`` in the order of
      batch, sparse, and dense dimensions. The i’th axis of the returned array
      corresponds to the axis numbered permutation[i] of ``mat``. Transpose
      permutation currently does not support permuting batch axes with non-batch
      axes nor permuting dense axes with non-dense axes.

  Returns:
    A BCOO-format array.
  """
  buffers = _bcoo_transpose(mat.data, mat.indices, permutation=permutation, spinfo=mat._info)
  out_shape = tuple(mat.shape[p] for p in permutation)
  return BCOO(buffers, shape=out_shape, unique_indices=mat.unique_indices)

