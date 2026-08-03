from typing import Any

def named_sharding_to_xla_hlo_sharding(
    self, num_dimensions: int) -> xc.HloSharding:
  mesh, spec = get_non_one_sized_mesh_spec(self.mesh, self.spec)
  mesh_shape = mesh.shape
  array_mapping = get_array_mapping(spec)
  mesh_axis_pos = {name: i for i, name in enumerate(mesh.axis_names)}

  special_axes = {}
  if (manual_axes := frozenset(mesh.manual_axes)):
    axis_names = mesh.axis_names
    for manual_axis in manual_axes:
      special_axes[axis_names.index(manual_axis)] = xc.OpSharding.Type.MANUAL

  if (unreduced_axes := spec.unreduced):
    axis_names = mesh.axis_names
    for u in unreduced_axes:
      special_axes[axis_names.index(u)] = xc.OpSharding.Type.UNREDUCED

  replicated_mesh_axes = []
  for i, (axis_name, axis_val) in enumerate(mesh_shape.items()):
    if axis_name not in array_mapping:
      replicated_mesh_axes.append((i, axis_val))

  if len(replicated_mesh_axes) == len(mesh_shape) and not special_axes:
    return xc.HloSharding.replicate()

  mesh_permutation = []
  new_mesh_shape = [1] * num_dimensions
  for name, pos in sorted(array_mapping.items(), key=lambda x: x[1]):
    new_mesh_shape[pos] *= mesh_shape[name]
    mesh_permutation.append(mesh_axis_pos[name])

  last_tile_dims = []
  if replicated_mesh_axes:
    axes_by_type: dict[Any, list[int]] = collections.defaultdict(list)
    size_by_type = collections.defaultdict(lambda: 1)
    assert {x[0] for x in replicated_mesh_axes}.issuperset(set(special_axes.keys()))
    for i, size in replicated_mesh_axes:
      ty = special_axes.get(i, xc.OpSharding.Type.REPLICATED)
      axes_by_type[ty].append(i)
      size_by_type[ty] *= size
    for ty, axes in sorted(axes_by_type.items(), key=lambda x: x[0].value):
      last_tile_dims.append(ty)
      new_mesh_shape.append(size_by_type[ty])
      mesh_permutation.extend(axes)

  # Explanation of the parameters of `HloSharding.iota_tile`.
  # This is the HloShardingV2 format:
  #   * dims: How many ways each dimension is sharded.
  #       Replicated/Manual dims are added added at the end
  #   * reshape_dims: This is the just the shape of the mesh.
  #   * transpose_perm: This is the order in which mesh axes in PartitionSpec
  #       appear relative to mesh.axis_names order.
  #   * subgroup_types: List of type of OpSharding. Type can be REPLICATED and MANUAL.
  # Let's see an example:
  #   Consider input_shape=(8, 4, 2, 2), mesh={'a': 2, 'b': 2, 'c': 2, 'd': 2}
  #   and partition_spec=P(None, ('d', 'b'), 'c').
  #   Arguments to iota_tile will be:
  #     dims = [1, 4, 2, 1, 2]  # 'a' is replicated hence `2` is at the end.
  #     reshape_dims = [2, 2, 2, 2]
  #     transpose_perm = [3, 1, 2, 0]  # 'a' is replicated hence 0 is at the end
  #     subgroup_types = [xc.OpSharding.Type.REPLICATED]
  dims = new_mesh_shape
  reshape_dims = mesh.axis_sizes
  if self._logical_device_ids is None:
    return xc.HloSharding.iota_tile(
        dims=dims, reshape_dims=reshape_dims, transpose_perm=mesh_permutation,
        subgroup_types=last_tile_dims)
  else:
    return xc.HloSharding.subgroup_with_device_ordering(
        np.asarray(self._logical_device_ids)
        .reshape(dims).reshape(reshape_dims).transpose(mesh_permutation)
        .reshape(dims), subgroup_types=last_tile_dims)

