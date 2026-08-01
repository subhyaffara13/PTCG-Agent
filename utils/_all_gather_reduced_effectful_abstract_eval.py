
def _all_gather_reduced_effectful_abstract_eval(
    x_aval, *, all_gather_dimension, axis_name, axis_size, tiled
):
  _check_axis_names(axis_name, 'all_gather_reduced')
  if not x_aval.mat.varying:
    raise ValueError('all_gather_reduced only accepts inputs that are'
                     f' varying. Got {x_aval.str_short(True)}')
  # If the intersection between x.mat.varying and axis_name is empty, error
  if not (x_aval.mat.varying & set(axis_name)):
    raise ValueError(
        'all_gather_reduced is a Varying -> Reduced collective. This means '
        f'that the {axis_name=} passed to `all_gather_reduced` must be present '
        f'in jax.typeof(x).mat.varying={x_aval.mat.varying}')
  if x_aval.mat.reduced & set(axis_name):
    raise ValueError(
        "all_gather_reduced's input cannot be reduced across the axis_name"
        f" provided. Got x={x_aval.str_short(True)} and {axis_name=}")

  new_shape = list(x_aval.shape)
  if tiled:
    new_shape[all_gather_dimension] *= axis_size
  else:
    new_shape.insert(all_gather_dimension, axis_size)

  new_reduced = x_aval.mat.reduced | frozenset(axis_name)
  out_vma = frozenset(v for v in x_aval.mat.varying if v not in axis_name)
  out_mat = x_aval.mat.update(varying=out_vma, reduced=new_reduced)
  return (x_aval.update(shape=new_shape, manual_axis_type=out_mat),
          {*map(core.NamedAxisEffect, axis_name)})

