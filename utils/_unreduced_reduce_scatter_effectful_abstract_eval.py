
def _unreduced_reduce_scatter_effectful_abstract_eval(
    x_aval, *, axis_name, scatter_dimension, axis_size, tiled
):
  _check_axis_names(axis_name, 'reduce_scatter')
  if not x_aval.mat.unreduced:
    raise ValueError('unreduced_psum_scatter only accepts inputs that are'
                     f' unreduced. Got {x_aval.str_short(True)}')
  # If intersection between x.unreduced & axis_name is empty, error
  if not (x_aval.mat.unreduced & frozenset(axis_name)):
    raise ValueError(
        "unreduced_psum_scatter is a Unreduced -> Varying collective. This"
        f" means that the {axis_name=} passed to `unreduced_psum_scatter` must"
        " be present in"
        f" jax.typeof(x).mat.unreduced={x_aval.mat.unreduced}"
    )
  if x_aval.mat.varying & set(axis_name):
    raise ValueError(
        "unreduced_psum_scatter's input cannot be varying across the axis_name"
        f" provided. Got x={x_aval.str_short(True)} and {axis_name=}")

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

  out_unreduced = frozenset(i for i in x_aval.mat.unreduced
                            if i not in axis_name)
  out_vma = x_aval.mat.varying | set(axis_name)
  out_mat = x_aval.mat.update(varying=out_vma, unreduced=out_unreduced)
  return (x_aval.update(shape=new_shape, manual_axis_type=out_mat),
          {*map(core.NamedAxisEffect, axis_name)})

