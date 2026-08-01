
def _all_gather_invariant_effectful_abstract_eval(
    x_aval, *, all_gather_dimension, axis_name, axis_size, tiled
):
  _check_axis_names(axis_name, 'all_gather_invariant')
  check_unreduced_args([x_aval], axis_name, 'all_gather_invariant')
  new_shape = list(x_aval.shape)
  if tiled:
    new_shape[all_gather_dimension] *= axis_size
  else:
    new_shape.insert(all_gather_dimension, axis_size)
  out_vma = frozenset(v for v in x_aval.mat.varying if v not in axis_name)
  return (x_aval.update(shape=new_shape,
                        manual_axis_type=x_aval.mat.update(varying=out_vma)),
          {*map(core.NamedAxisEffect, axis_name)})

