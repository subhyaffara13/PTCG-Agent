
def _reduce_scatter_effectful_abstract_eval(
    x_aval, *, axis_name, scatter_dimension, axis_index_groups, axis_size, tiled
):
  if not isinstance(axis_name, (list, tuple)):
    axis_name = (axis_name,)
  _check_axis_names(axis_name, 'reduce_scatter')
  check_unreduced_args([x_aval], axis_name, 'reduce_scatter')
  new_shape = list(x_aval.shape)
  scatter_dim_input_size = x_aval.shape[scatter_dimension]
  if tiled:
    if scatter_dim_input_size % axis_size != 0:
      raise ValueError(f"tiled reduce_scatter operand scatter dimension size "
                       f"{scatter_dim_input_size} must be divisible by "
                       f"shard_count {axis_size}")
    new_shape[scatter_dimension] = scatter_dim_input_size // axis_size
  else:
    if scatter_dim_input_size != axis_size:
      raise ValueError(f"reduce_scatter operand scatter dimension size "
                       f"{scatter_dim_input_size} must match shard count "
                       f"{axis_size}")
    del new_shape[scatter_dimension]
  vma = collective_vma_rule('reduce_scatter', axis_name, x_aval)
  return (x_aval.update(shape=new_shape,
                        manual_axis_type=x_aval.mat.update(varying=vma)),
          {*map(core.NamedAxisEffect, axis_name)})

