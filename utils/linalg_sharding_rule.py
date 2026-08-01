
def linalg_sharding_rule(
    multiple_results, shape_rule, ranks, name, *avals, **kwargs
):
  output_shapes = shape_rule(*avals, **kwargs)
  batch_specs = []
  for i, (rank, aval) in enumerate(zip(ranks, avals)):
    spec = aval.sharding.spec
    batch_spec, rest_spec = spec[:len(spec) - rank], spec[len(spec) - rank:]
    if not all(s is None for s in rest_spec):
      raise core.ShardingTypeError(
          f"Input {i} to {name} must be unsharded on non-batch dimensions, "
          f"but got {spec}."
      )
    batch_specs.append(batch_spec)
  batch_spec = batch_specs[0]
  if any(b != batch_spec for b in batch_specs[1:]):
    raise core.ShardingTypeError(
        f"All inputs to {name} must have the same batch sharding, but got "
        f"{batch_specs}.")
  sharding = avals[0].sharding
  if multiple_results:
    def p(s): return P(*batch_spec, *((None,) * (len(s) - len(batch_spec))))
    return [sharding.update(spec=p(s)) for s in output_shapes]
  else:
    ndim = len(output_shapes) - len(batch_spec)
    return sharding.update(spec=P(*(tuple(batch_spec) + (None,) * ndim)))

