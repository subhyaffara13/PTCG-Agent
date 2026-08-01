
def _split_merge_singleton_dim_sharding_rule(operand, new_sizes):
  filtered_spec = [sp for sh, sp in zip(operand.shape, operand.sharding.spec)
                   if sh != 1]
  fs = iter(filtered_spec)
  new_spec = []
  for n in new_sizes:
    if n == 1:
      new_spec.append(None)
    else:
      sp = next(fs)
      new_spec.append(sp)
  return operand.sharding.update(spec=new_spec)

