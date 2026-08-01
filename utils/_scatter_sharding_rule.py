
def _scatter_sharding_rule(
    operand, indices, updates, *, update_jaxpr, update_consts,
    dimension_numbers, indices_are_sorted, unique_indices, mode):
  out_mesh = _resolve_mesh(
      *(x.sharding.mesh for x in (operand, indices, updates)))
  out_spec = _scatter_spec_computation(operand, indices, updates,
                                       dimension_numbers)
  if out_spec is None:
    raise core.ShardingTypeError(
        "Use `.at[...].set/add/mul/...(out_sharding=)` to provide output"
        " PartitionSpec for the scatter update as out sharding could not be"
        " resolved unambiguously (or would require collectives on inputs). Got"
        f" {operand=}, {indices=}, {updates=}")
  return NamedSharding(out_mesh, out_spec)

