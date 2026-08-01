
def insert_collective_pvary(axis_name, x):
  if not config.auto_pcast.value or not config._check_vma.value:
    return x
  axis_name = (axis_name,) if not isinstance(axis_name, tuple) else axis_name
  aval = core.typeof(x)
  names_union = set(axis_name) | aval.mat.varying
  x = pvary(x, tuple(n for n in names_union if n not in aval.mat.varying))
  return x

