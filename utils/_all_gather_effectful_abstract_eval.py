
def _all_gather_effectful_abstract_eval(
    x_aval, *, all_gather_dimension, axis_name, axis_index_groups, axis_size, tiled
):
  if not isinstance(axis_name, (list, tuple)):
    axis_name = (axis_name,)
  _check_axis_names(axis_name, 'all_gather')
  check_unreduced_args([x_aval], axis_name, 'all_gather')
  new_shape = list(x_aval.shape)
  if tiled:
    new_shape[all_gather_dimension] *= axis_size
  else:
    new_shape.insert(all_gather_dimension, axis_size)
  out_vma = collective_vma_rule('all_gather', axis_name, x_aval)
  return (x_aval.update(shape=new_shape,
                        manual_axis_type=x_aval.mat.update(varying=out_vma)),
          {*map(core.NamedAxisEffect, axis_name)})

