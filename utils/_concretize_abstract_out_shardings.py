
def _concretize_abstract_out_shardings(shardings, avals, device_assignment,
                                       out_mem_kinds):
  if device_assignment is None:
    return shardings

  out: list[UnspecifiedValue | JSharding] = []
  for s, a, mem_kind in zip(shardings, avals, out_mem_kinds):
    if isinstance(s, UnspecifiedValue) and isinstance(a, core.ShapedArray):
      if a.sharding.mesh.empty:
        out.append(s)
      elif a.sharding.mesh._are_all_axes_auto_or_manual:
        out.append(s)
      else:
        spec = (PartitionSpec(*[PartitionSpec.UNCONSTRAINED if sp is None else sp
                                for sp in a.sharding.spec])
                if a.sharding.mesh._any_axis_auto else a.sharding.spec)
        out.append(NamedSharding(
            _abstract_to_concrete_mesh(a.sharding.mesh, device_assignment),
            spec, memory_kind=mem_kind))
    else:
      out.append(s)
  return tuple(out)

