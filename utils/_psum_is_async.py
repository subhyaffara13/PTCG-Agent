
def _psum_is_async(x, axis_name, *, axis_index_groups=None, is_async=False):
  axes = ((axis_name,) if not isinstance(axis_name, (tuple, list)) else
          tuple(axis_name))
  # TODO(yashkatariya): Remove this handling and remove_size_one_mesh_axis_from_type
  # generally from JAX.
  axes = _maybe_skip_one_sized_axes(axes)
  if not axes:
    return x
  def bind(leaf):
    from_ = _get_from(core.typeof(leaf), axes, 'jax.lax.psum')
    if from_ == 'unreduced':
      if axis_index_groups is not None:
        raise NotImplementedError
      return unreduced_psum(leaf, axes, is_async)
    else:
      return _psum(leaf, axes, axis_index_groups=axis_index_groups,
                   is_async=is_async)
  return tree_util.tree_map(bind, x)

