
def modify_spec_for_auto_manual(spec, mesh) -> P:
  new_spec: list[Any] = []
  # PartitionSpec can only mention mesh axes that are Explicit.
  for s in spec.partitions:
    if s is None:
      new_spec.append(s)
    elif isinstance(s, tuple):
      new_spec.append(tuple(
          p for p in s if mesh._name_to_type[p] == AxisType.Explicit))
    else:
      new_spec.append(s if mesh._name_to_type[s] == AxisType.Explicit else None)
  new_unreduced = {u for u in spec.unreduced
                   if mesh._name_to_type[u] == AxisType.Explicit}
  new_reduced = {u for u in spec.reduced
                 if mesh._name_to_type[u] == AxisType.Explicit}
  return P(*new_spec, unreduced=new_unreduced, reduced=new_reduced)

