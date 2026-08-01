
def block_id_to_grid_id(ctx: LoweringRuleContext,
                        block_ids: Sequence[ir.Value],
                        axis_name: Hashable):
  squashed_dims = ctx.module_ctx.squashed_dims
  axis_names = ctx.module_ctx.axis_names
  if squashed_dims:
    unsquashed_names = axis_names.grid[:2]
    squashed_names = axis_names.grid[2:]
  else:
    # These are unused but initialized for type checkers.
    unsquashed_names = squashed_names = ()

  if squashed_dims:
    if axis_name in unsquashed_names:
      # We reversed the grid and cluster axes.
      # e.g. for the grid (a, b, c, d, wg)
      # squashed = (a, b)  Mapped to Dimension.z (2)
      # unsquashed = (c, d)  Mapped to Dimension.y (1) and Dimension.x (0)
      idx = unsquashed_names.index(axis_name)
      return block_ids[gpu_dialect.Dimension(idx)]
    else:
      assert axis_name in squashed_names
      # All squashed dimensions are mapped to Dimension.z.
      axis = squashed_names.index(axis_name)
      return _unravel_program_id(
          _as_index(block_ids[gpu_dialect.Dimension.z]), axis, squashed_dims
      )
  else:
    assert axis_name in axis_names.grid
    idx = axis_names.grid.index(axis_name)
    return block_ids[gpu_dialect.Dimension(idx)]

