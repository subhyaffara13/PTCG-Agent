
def _check_mesh_resource_axis(mesh, pspec):
  for p in pspec.partitions:
    if p is PartitionSpec.UNCONSTRAINED or p is None:
      continue
    p = p if isinstance(p, tuple) else (p,)
    for r in p:
      if r not in mesh.axis_names:
        raise ValueError(
            f"Resource axis: {r} of {pspec} "
            f"is not found in mesh: {tuple(mesh.shape.keys())}.")
  if (AxisType.Auto not in mesh.axis_types and
      PartitionSpec.UNCONSTRAINED in pspec.partitions):
    raise ValueError(
        f'{pspec} cannot contain'
        ' `P.UNCONSTRAINED` when no mesh axis_types are `Auto`. Got mesh'
        f' axis_types: {mesh.axis_types}')

