
def _merge_an_axis_sharding_rule(operand, operand_merge, new_sizes, dimensions):
  new_spec = []
  mesh = operand.sharding.mesh
  op_spec = iter(operand.sharding.spec)
  for ns, op_merge in zip(new_sizes, operand_merge):
    if isinstance(op_merge, list):
      tup_sp = tuple(next(op_spec) for _ in op_merge)
      if all(s is None for s in tup_sp):
        new_spec.append(None)
      elif dimensions is None:
        tup_sp = strip_trailing_nones(flatten_spec(tup_sp))
        if None in tup_sp:
          raise_reshape_error(operand, new_sizes)
        partitions = split_partitions(mesh, tup_sp, [ns], operand, new_sizes)
        new_spec.extend(partitions)
      else:
        raise_reshape_error(operand, new_sizes)
    else:
      new_spec.append(next(op_spec))
  assert next(op_spec, None) is None
  assert len(new_spec) == len(new_sizes), (new_spec, new_sizes)
  return operand.sharding.update(spec=new_spec)

