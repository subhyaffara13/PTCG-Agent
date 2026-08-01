
def _axis_index_effectful_abstract_eval(*, axis_name):
  effect = {core.NamedAxisEffect(axis_name)}
  axis_name = (axis_name,) if not isinstance(axis_name, tuple) else axis_name
  _check_axis_names(axis_name, 'axis_index')
  mesh = get_abstract_mesh()
  sharding = NamedSharding(mesh, P())
  vma = ((frozenset(axis_name) if mesh._any_axis_manual else frozenset())
         if config._check_vma.value else frozenset())
  out_mat = core.ManualAxisType(varying=vma)
  out_aval = ShapedArray((), np.int32, sharding=sharding, manual_axis_type=out_mat)
  return out_aval, effect

