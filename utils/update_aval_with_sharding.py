
def update_aval_with_sharding(aval, sharding, mat=None):
  if isinstance(sharding, NamedSharding):
    s = NamedSharding(sharding.mesh.abstract_mesh,
                      sharding.spec._normalized_spec_for_aval(aval.ndim))
    return aval.update(
        sharding=s, manual_axis_type=(aval.mat if mat is None else mat),
        memory_space=mem_kind_to_space(sharding.memory_kind))
  return aval if mat is None else aval.update(manual_axis_type=mat)

