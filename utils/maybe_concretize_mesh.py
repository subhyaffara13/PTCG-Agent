
def maybe_concretize_mesh(sharding, da: xc.DeviceList):
  if (isinstance(sharding, NamedSharding) and
      isinstance(sharding.mesh, AbstractMesh)):
    if sharding.mesh.size != len(da):
      raise ValueError(
          f"The size of abstract mesh {sharding.mesh.size} in {sharding} must"
          f" match the length of device assignment: {len(da)}")
    return sharding.update(mesh=_abstract_to_concrete_mesh(sharding.mesh, da))
  return sharding

