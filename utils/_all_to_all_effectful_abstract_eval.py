
def _all_to_all_effectful_abstract_eval(
    input_aval, axis_name, split_axis, concat_axis, axis_index_groups, tiled
):
  del tiled  # expand_dims and squeeze is done in `all_to_all` if `True`
  if isinstance(axis_name, list):
    axis_name = tuple(axis_name)
  elif not isinstance(axis_name, tuple):
    axis_name = (axis_name,)
  _check_axis_names(axis_name, 'all_to_all')
  check_unreduced_args([input_aval], axis_name, 'all_to_all')
  shape = list(input_aval.shape)
  axis_size = (
      _axis_size(axis_name)
      if axis_index_groups is None
      else len(axis_index_groups[0])
  )
  assert shape[split_axis] % axis_size == 0, (shape[split_axis], axis_size)
  shape[split_axis] //= axis_size
  shape[concat_axis] *= axis_size
  vma = collective_vma_rule('all_to_all', axis_name, input_aval)
  out_aval = input_aval.update(
    shape=tuple(shape), weak_type=False,
    manual_axis_type=input_aval.mat.update(varying=vma))
  effects = {*map(core.NamedAxisEffect, axis_name)}
  return out_aval, effects

