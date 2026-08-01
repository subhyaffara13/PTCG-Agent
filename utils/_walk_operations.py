
def _walk_operations(op, k):
  k -= 1
  if k < 0:
    return k
  for region in op.regions:
    for block in region:
      for child_op in block:
        k = _walk_operations(child_op, k)
        if k < 0:
          return k
  return k

