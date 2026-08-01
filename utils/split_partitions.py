
def split_partitions(mesh, tup_sp, out, operand, new_sizes):
  iter_sp = iter(tup_sp)
  partitions = []
  for o in out:
    dim_partitions = []
    while o > 1:
      ns = next(iter_sp, None)
      if ns is None:
        break
      axis_size = mesh.shape[ns]
      o, remainder = divmod(o, axis_size)
      if remainder != 0:
        raise_reshape_error(operand, new_sizes)
      dim_partitions.append(ns)
    partitions.append(tuple(dim_partitions))
  assert next(iter_sp, None) is None
  return partitions

