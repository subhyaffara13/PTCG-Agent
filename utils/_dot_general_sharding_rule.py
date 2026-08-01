
def _dot_general_sharding_rule(lhs, rhs, *, dimension_numbers, precision,
                               preferred_element_type: DTypeLike | None,
                               out_sharding):
  if (not lhs.sharding.mesh.empty and not rhs.sharding.mesh.empty and
      lhs.sharding.mesh != rhs.sharding.mesh):
    raise core.ShardingTypeError(
        'Mesh of both lhs and rhs should match. Got lhs:'
        f' {lhs.sharding.mesh} and rhs: {rhs.sharding.mesh}')

  if out_sharding is not None:
    assert isinstance(out_sharding, NamedSharding)
    return out_sharding

  (lhs_contracting, rhs_contracting), (lhs_batch, rhs_batch) = dimension_numbers
  lhs_contracting_spec = tuple(lhs.sharding.spec.partitions[i]
                               for i in lhs_contracting)
  rhs_contracting_spec = tuple(rhs.sharding.spec.partitions[i]
                               for i in rhs_contracting)

  lhs_batch_spec = tuple(lhs.sharding.spec.partitions[i] for i in lhs_batch)
  rhs_batch_spec = tuple(rhs.sharding.spec.partitions[i] for i in rhs_batch)
  msg = ("dot_general requires lhs batch dimensions and rhs batch dimensions "
        f"to have the consistent sharding, got {lhs_batch_spec} and "
        f"{rhs_batch_spec}.")
  _check_specs_match(lhs_batch_spec, rhs_batch_spec, msg)

  msg = ("dot_general requires contracting dimensions to have consistent "
        f"sharding, got {lhs_contracting_spec} and {rhs_contracting_spec}.")
  _check_specs_match(lhs_contracting_spec, rhs_contracting_spec, msg)

  for l, r in zip(lhs_contracting_spec, rhs_contracting_spec):
    if l is not None and r is not None:
      raise core.ShardingTypeError(
          'Contracting dimensions are sharded and it is ambiguous how the'
          ' output should be sharded. Please specify the output sharding via'
          ' the `out_sharding` parameter.'
          f' Got {lhs_contracting_spec=} and {rhs_contracting_spec=}')

  if lhs.sharding.mesh.empty and not rhs.sharding.mesh.empty:
    mesh = rhs.sharding.mesh
  else:
    mesh = lhs.sharding.mesh
  return _dot_general_sharding_computation(
      lhs.sharding.spec, rhs.sharding.spec, dimension_numbers, mesh)

