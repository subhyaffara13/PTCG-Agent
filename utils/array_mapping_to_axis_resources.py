
def array_mapping_to_axis_resources(array_mapping: ArrayMapping):
  if not array_mapping:
    return PartitionSpec()
  max_index = -1
  reverse_map = collections.defaultdict(list)
  for axis, index in array_mapping.items():
    reverse_map[index].append(axis)
    if index > max_index:
      max_index = index
  partitions: list[MeshAxisName | None] = []
  for i in range(max_index + 1):
    axis = reverse_map[i]
    if axis:
      partitions.append(axis[0] if len(axis) == 1 else tuple(axis))
    else:
      partitions.append(None)
  return PartitionSpec(*partitions)

