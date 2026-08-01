
def _gather_sharding_rule(operand, indices, *, dimension_numbers,
                          slice_sizes, unique_indices, indices_are_sorted,
                          mode, fill_value):
  out_mesh = _resolve_mesh(operand.sharding.mesh, indices.sharding.mesh)
  out_spec = _gather_spec_computation(operand, indices, dimension_numbers,
                                      slice_sizes)
  if out_spec is None:
    raise core.ShardingTypeError(
        "Use `.at[...].get(out_sharding=)` to provide output PartitionSpec for"
        " the gather indexing as out sharding could not be resolved"
        " unambiguously (or would require collectives on inputs). Got"
        f" {operand=}, {indices=}")
  return NamedSharding(out_mesh, out_spec)

