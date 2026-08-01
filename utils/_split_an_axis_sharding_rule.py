
def _split_an_axis_sharding_rule(operand, out_split, new_sizes, dimensions):
  new_spec = []
  mesh = operand.sharding.mesh
  for out, sp in zip(out_split, operand.sharding.spec.partitions):
    if isinstance(out, list):
      if sp is None:
        new_spec.extend([None] * len(out))
      elif dimensions is None:
        tup_sp = sp if isinstance(sp, tuple) else (sp,)
        partitions = split_partitions(mesh, tup_sp, out, operand, new_sizes)
        new_spec.extend(partitions)
      else:
        raise_reshape_error(operand, new_sizes)
    else:
      new_spec.append(sp)
  assert len(new_spec) == len(new_sizes), (new_spec, new_sizes)
  return operand.sharding.update(spec=new_spec)

