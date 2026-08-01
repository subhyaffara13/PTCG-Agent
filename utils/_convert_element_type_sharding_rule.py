
def _convert_element_type_sharding_rule(operand, *, new_dtype, weak_type,
                                        sharding):
  if sharding is None:
    return operand.sharding
  if sharding._is_concrete:
    if isinstance(sharding, NamedSharding):
      return NamedSharding(sharding.mesh.abstract_mesh, sharding.spec)
    else:
      return core.get_cur_mesh_sharding()
  return sharding

