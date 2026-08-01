
def _check_unique_resources(pspec: PartitionSpec, arg_name: str, mesh=None
                            ) -> None:
  resource_counts: dict[MeshAxisName, int] = {}
  duplicate = False
  for d in pspec.partitions:
    if d is PartitionSpec.UNCONSTRAINED or d is None:
      continue
    d = d if isinstance(d, tuple) else (d,)
    for resource in d:
      count = resource_counts.get(resource, 0)
      if count > 0:
        duplicate = True
      resource_counts[resource] = count + 1
  if duplicate:
    multiple_uses = [r for r, c in resource_counts.items() if c > 1]
    raise DuplicateSpecError(
        message=(
            f'A single {arg_name} specification can map every mesh axis to at'
            f' most one positional dimension, but {pspec} has duplicate entries'
            f' for {mesh_lib.show_axes(multiple_uses)}'),
        mesh=mesh, pspec=pspec)

