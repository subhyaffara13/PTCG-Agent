
def _ref_group_tmem_col_size(refs: _GPUMemoryRefTree) -> int:
  """Returns the total number of TMEM columns used by a group of aliased Refs.
  """
  ncols = 0
  for ref in jax.tree.leaves(refs):
    ref_ncols = ref.layout.cols_in_shape(ref.shape,
                                         dtypes.itemsize_bits(ref.dtype))
    ncols += align_to(ref_ncols, TMEM_COL_ALIGNMENT)
  return ncols

