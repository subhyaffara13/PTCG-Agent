
def _allreduce_effectful_abstract_eval(aval, *, axes, axis_index_groups):
  _check_axis_names(axes, 'psum')
  named_axes = tuple(axis for axis in axes if not isinstance(axis, int))
  pos_axes = tuple(axis for axis in axes if isinstance(axis, int))
  if axis_index_groups is not None:
    if len(pos_axes) != 0:
      raise ValueError(f"axis_index_groups can only be used with reductions over "
                       f"named axes, but got: {axes}")
  core.check_avals_context_mesh([aval], 'psum')
  check_unreduced_args([aval], axes, 'psum')
  out_aval = ShapedArray(
      lax._reduce_op_shape_rule(aval, axes=pos_axes), aval.dtype,
      sharding=lax._reduce_op_sharding_rule(aval, axes=pos_axes))
  return out_aval, {core.NamedAxisEffect(axis) for axis in named_axes}

