import math


def axis_groups(axis_ctx, name) -> tuple[tuple[int, ...]]:
  assert not isinstance(axis_ctx, sharding_impls.ShardingContext)
  size = axis_ctx.mesh.size
  axis_names = axis_ctx.mesh.axis_names
  axis_sizes = axis_ctx.mesh.axis_sizes
  if not isinstance(name, (list, tuple)):
    name = (name,)
  mesh_axes = tuple(unsafe_map(partial(_axis_read, axis_names), name))
  trailing_size, ragged = divmod(size, math.prod(axis_sizes))
  assert not ragged
  mesh_spec = axis_sizes + (trailing_size,)
  return _axis_groups(mesh_spec, mesh_axes)

