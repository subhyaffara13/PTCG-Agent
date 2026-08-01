
def _with_sharding_constraint_one_fallback(
  axis_resources: LogicalPartitionSpec,
  x: Array,
  fallback: RulesFallback = RulesFallback.AXIS_IS_UNSHARDED,
  rules: LogicalRules | None = None,
  mesh: jax.sharding.Mesh | None = None,
):
  """Either imposes a sharding constraint or applies fallback."""
  mesh_axes = _logical_to_mesh_axes(axis_resources, rules)
  if mesh_axes is None:
    return _with_sharding_constraint(x, None, mesh=mesh)

  if fallback == RulesFallback.AXIS_IS_UNSHARDED:
    mesh_axes = [None if x is _unassigned_axis else x for x in mesh_axes]
  else:
    if any(x is _unassigned_axis for x in mesh_axes):
      if fallback == RulesFallback.RAISE_ERROR:
        raise ValueError(f'Axis names {axis_resources} did not match a rule')
      else:
        return x
  return _with_sharding_constraint(
    x, jax.sharding.PartitionSpec(*mesh_axes), mesh=mesh
  )

