
def spmd_names_insert_pvary(*args):
  if not config.auto_pcast.value:
    return args
  if (config._check_vma.value and
      (spmd_names := core.get_axis_env().spmd_axis_names)):
    return [core.pvary(a, tuple(spmd_names - aval.mat.varying))
            if isinstance(aval := typeof(a), core.ShapedArray) else a
            for a in args]
  return args

