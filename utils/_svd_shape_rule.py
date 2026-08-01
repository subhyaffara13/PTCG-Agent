
def _svd_shape_rule(shape, *, full_matrices, compute_uv, subset_by_index, **_):
  m, n = shape
  rank = core.min_dim(m, n)
  if subset_by_index is not None:
    if full_matrices and subset_by_index != (0, rank):
      raise ValueError("full_matrices and subset_by_index cannot both be set")
    rank = core.min_dim(rank, subset_by_index[1] - subset_by_index[0])
  if compute_uv:
    return (
        (rank,),
        (m, m if full_matrices else rank),
        (n if full_matrices else rank, n),
    )
  else:
    return (rank,),

