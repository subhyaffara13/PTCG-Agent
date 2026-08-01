
def shard_value(value, out_sharding, sharding_rules, mesh):
  if not out_sharding:
    return value

  if mesh is None:
    mesh = meta.get_global_mesh()

  out_sharding = apply_rules(out_sharding, sharding_rules)

  sharding_mesh = get_mesh(out_sharding)

  if sharding_mesh:
    if mesh:
      assert mesh == out_sharding.mesh
    mesh = sharding_mesh

  if mesh is None:
    raise ValueError(
      'An auto mesh context or metadata is required if creating a variable'
      f' with annotation {out_sharding=}. '
      'For more guidance, see https://flax.readthedocs.io/en/latest/flip/4844-var-eager-sharding.html.')

  if isinstance(out_sharding, PartitionSpec):
    out_sharding = NamedSharding(mesh, out_sharding)

  return _apply_sharding(value, out_sharding, mesh)

