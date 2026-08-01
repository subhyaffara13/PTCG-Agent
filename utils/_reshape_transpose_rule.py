
def _reshape_transpose_rule(ct, operand, *, new_sizes, dimensions, sharding):
  assert ad.is_undefined_primal(operand)
  if dimensions is None:
    return [reshape(ct, operand.aval.shape, out_sharding=operand.aval.sharding)]
  else:
    new_sizes = tuple(operand.aval.shape[d] for d in dimensions)
    new_partitions = tuple(operand.aval.sharding.spec[d] for d in dimensions)
    ct_s = operand.aval.sharding.update(
        spec=operand.aval.sharding.spec.update(partitions=new_partitions))
    out = reshape(ct, new_sizes, out_sharding=ct_s)
    return [transpose(out, np.argsort(dimensions))]

