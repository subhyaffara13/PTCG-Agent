
def _psum_scatter(x, axis_name, *, scatter_dimension, axis_index_groups, tiled,
                  is_async):
  if not isinstance(axis_name, tuple):
    axis_name = (axis_name,)
  if not axis_name:
    return x
  axis_size = _axis_size(axis_name, axis_index_groups)
  axis_index_groups = _canonicalize_axis_index_groups(axis_index_groups)
  def bind(leaf):
    leaf = insert_collective_pvary(axis_name, leaf)
    prim = reduce_scatter_start_p if is_async else reduce_scatter_p
    return prim.bind(
        leaf, axis_name=axis_name, scatter_dimension=scatter_dimension,
        axis_index_groups=axis_index_groups, axis_size=axis_size, tiled=tiled)
  return tree_util.tree_map(bind, x)

