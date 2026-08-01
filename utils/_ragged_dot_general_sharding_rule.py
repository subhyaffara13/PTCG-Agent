
def _ragged_dot_general_sharding_rule(
    lhs, rhs, group_sizes, *, ragged_dot_dimension_numbers, precision,
    preferred_element_type: DTypeLike | None, group_offset, out_sharding):
  mesh_set = {x.sharding.mesh for x in [lhs, rhs, group_sizes]
              if not x.sharding.mesh.empty}
  if len(mesh_set) > 1:
    raise core.ShardingTypeError(
      'All argument meshes must be the same or unspecified, but got'
      f' lhs mesh = {lhs.sharding.mesh}, rhs mesh = {rhs.sharding.mesh},'
      f' group_sizes mesh = {group_sizes.sharding.mesh}')

  if out_sharding is None:
    raise NotImplementedError(
      "Explicit sharding inference for ragged_dot_general is not currently"
      " implemented. Please specify out_sharding.")
  return out_sharding

