
def get_sharding_for_vmap(axis_data, orig_sharding, axis):
  val = axis_data.explicit_mesh_axis
  new_spec = orig_sharding.spec.update(
      partitions=tuple_insert(orig_sharding.spec.partitions, axis, val))
  return orig_sharding.update(spec=new_spec)

