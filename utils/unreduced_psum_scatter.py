
def unreduced_psum_scatter(x, axis_name, *, scatter_dimension=0, tiled=False,
                           is_async=False):
  if not isinstance(axis_name, tuple):
    axis_name = (axis_name,)
  if not axis_name:
    return x
  axis_size = _axis_size(axis_name, None)
  def bind(leaf):
    prim = (
        unreduced_reduce_scatter_start_p
        if is_async
        else unreduced_reduce_scatter_p
    )
    return prim.bind(
        leaf, axis_name=axis_name, scatter_dimension=scatter_dimension,
        axis_size=axis_size, tiled=tiled)
  return tree_util.tree_map(bind, x)

