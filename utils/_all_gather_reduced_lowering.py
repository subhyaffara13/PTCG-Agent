
def _all_gather_reduced_lowering(
    ctx, x, *, all_gather_dimension, axis_name, axis_size, tiled,
    platform=None, is_async=False):
  return _all_gather_lowering(
      ctx, x, all_gather_dimension=all_gather_dimension, axis_name=axis_name,
      axis_index_groups=None, axis_size=axis_size, tiled=tiled,
      platform=platform, is_async=is_async)

