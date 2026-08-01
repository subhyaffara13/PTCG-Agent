
def _dot_general_pull_rule(
    ctx: PullRuleContext,
    block_transform: BlockIndexTransform,
    *,
    dimension_numbers,
    **_,
) -> Sequence[BlockIndexTransform]:
  if block_transform is no_block_index_transform:
    return [no_block_index_transform, no_block_index_transform]

  lhs_aval, rhs_aval = ctx.avals_in
  assert isinstance(lhs_aval, core.ShapedArray)
  assert isinstance(rhs_aval, core.ShapedArray)

  # Check assumptions: strictly 2D and no batch dimensions
  if not lhs_aval.ndim == 2 or not rhs_aval.ndim == 2:
    raise NotImplementedError('Only 2D dot_general supported.')
  (lhs_contracting, rhs_contracting), (lhs_batch, rhs_batch) = dimension_numbers
  if lhs_batch or rhs_batch:
    raise NotImplementedError('Batch dimensions not supported')
  if len(lhs_contracting) != 1 or len(rhs_contracting) != 1:
    raise NotImplementedError('Multiple contracting dimensions not supported')

  lc = lhs_contracting[0]
  rc = rhs_contracting[0]
  contraction_shape = lhs_aval.shape[lc]
  assert contraction_shape == rhs_aval.shape[rc]

  def make_transform(block_transform, contraction_index, out_index):
    nc_index = 1 - contraction_index

    def transform(*idxs):
      out_idx = block_transform.block_index_transform(*idxs)
      ret_idx = [None, None]
      # Contraction dimension is full, so we always have block index 0.
      ret_idx[contraction_index] = 0
      ret_idx[nc_index] = out_idx[out_index]
      return tuple(ret_idx)

    block_shape = [None, None]
    # Contraction dimension is full, so we use the full shape.
    block_shape[contraction_index] = contraction_shape
    block_shape[nc_index] = block_transform.block_shape[out_index]
    return BlockIndexTransform(
        block_shape=tuple(block_shape),
        block_index_transform=transform,
        pipeline_mode=block_transform.pipeline_mode,
    )

  lhs_block_transform = make_transform(block_transform, lc, 0)
  rhs_block_transform = make_transform(block_transform, rc, 1)
  return [lhs_block_transform, rhs_block_transform]

