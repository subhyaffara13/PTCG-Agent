
def _psum_scatter_is_async(x, axis_name, *, scatter_dimension=0,
                           axis_index_groups=None, tiled=False, is_async=False):
  axes = (axis_name,) if not isinstance(axis_name, tuple) else axis_name
  # TODO(yashkatariya): Remove this handling and remove_size_one_mesh_axis_from_type
  # generally from JAX.
  axes = _maybe_skip_one_sized_axes(axes)
  if not axes:
    return x
  def bind(leaf):
    from_ = _get_from(core.typeof(leaf), axes, 'jax.lax.psum_scatter')
    if from_ == 'unreduced':
      if axis_index_groups is not None:
        raise NotImplementedError
      return unreduced_psum_scatter(
          leaf, axes, scatter_dimension=scatter_dimension, tiled=tiled,
          is_async=is_async)
    else:
      return _psum_scatter(leaf, axes, scatter_dimension=scatter_dimension,
                           axis_index_groups=axis_index_groups, tiled=tiled,
                           is_async=is_async)
  return tree_util.tree_map(bind, x)

