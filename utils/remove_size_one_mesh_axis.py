
def remove_size_one_mesh_axis(spec, mesh) -> PartitionSpec:
  new_spec: list[Any] = []
  for s in spec.partitions:
    if s is None or s is PartitionSpec.UNCONSTRAINED:
      new_spec.append(s)
    elif isinstance(s, tuple):
      new_spec.append(tuple(i for i in s if mesh.shape[i] != 1))
    else:
      new_spec.append(None if mesh.shape[s] == 1 else s)
  unreduced = frozenset(u for u in spec.unreduced if mesh.shape[u] != 1)
  reduced = frozenset(r for r in spec.reduced if mesh.shape[r] != 1)
  return PartitionSpec(*new_spec, unreduced=unreduced, reduced=reduced)

