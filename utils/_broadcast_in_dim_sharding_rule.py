
def _broadcast_in_dim_sharding_rule(operand, *, shape, broadcast_dimensions,
                                    sharding):
  if sharding is not None:
    return sharding
  bds = set(broadcast_dimensions)
  orig_spec = iter(operand.sharding.spec.partitions)
  new_spec = [next(orig_spec) if i in bds else None for i in range(len(shape))]
  assert next(orig_spec, None) is None
  mesh = (get_abstract_mesh() if operand.sharding.mesh.empty else
          operand.sharding.mesh)
  return operand.sharding.update(
      mesh=mesh, spec=operand.sharding.spec.update(partitions=new_spec))

