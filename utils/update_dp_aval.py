
def update_dp_aval(aval, d):
  if not isinstance(aval, core.ShapedArray):
    return aval
  if isinstance(d, Sharding):
    aval = (aval.update(sharding=aval.sharding.update(mesh=d.mesh.abstract_mesh,
                                                      spec=d.spec))
            if isinstance(d, NamedSharding) else aval.update(sharding=None))
    if d.memory_kind is not None:
      aval = aval.update(memory_space=core.mem_kind_to_space(d.memory_kind))
    return aval
  elif isinstance(d, core.MemorySpace):
    return aval.update(memory_space=d)
  return aval

