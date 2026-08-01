
def get_array_mapping(axis_resources):
  if isinstance(axis_resources, UnspecifiedValue):
    return axis_resources
  d = collections.OrderedDict()
  for i, axes in enumerate(axis_resources.partitions):
    if axes is None or axes is PartitionSpec.UNCONSTRAINED:
      continue
    axes = axes if isinstance(axes, tuple) else (axes,)
    for axis in axes:
      d[axis] = i
  return d

