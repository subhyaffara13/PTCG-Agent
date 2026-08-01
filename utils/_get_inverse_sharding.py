
def _get_inverse_sharding(out_sharding, names, result_names):
  if len(result_names) > len(out_sharding.spec):
    out_sharding = out_sharding.update(spec=
        out_sharding.spec._normalized_spec_for_aval(len(result_names)))
  spec = out_sharding.spec
  inverse_spec = tuple(spec.partitions[result_names.index(name)]
                       for name in names)
  return NamedSharding(out_sharding.mesh, spec.update(partitions=inverse_spec))

