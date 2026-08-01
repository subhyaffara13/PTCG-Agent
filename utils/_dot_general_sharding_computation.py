
def _dot_general_sharding_computation(
    lhs_spec, rhs_spec, dimension_numbers, mesh):
  (lhs_contracting, rhs_contracting), (lhs_batch, rhs_batch) = dimension_numbers
  batch_spec = tuple(lhs_spec.partitions[i] for i in lhs_batch)
  lhs_contract_or_batch = tuple(sorted(tuple(lhs_contracting) + tuple(lhs_batch)))
  lhs_tensored_spec = tuple_delete(lhs_spec.partitions, lhs_contract_or_batch)
  rhs_contract_or_batch = tuple(sorted(tuple(rhs_contracting) + tuple(rhs_batch)))
  rhs_tensored_spec = tuple_delete(rhs_spec.partitions, rhs_contract_or_batch)
  return NamedSharding(mesh, P(*(batch_spec + lhs_tensored_spec + rhs_tensored_spec)))

