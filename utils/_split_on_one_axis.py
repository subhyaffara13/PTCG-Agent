
def _split_on_one_axis(op_shape, new_sizes):
  if len(new_sizes) <= len(op_shape):
    return False, []
  orig_op_shape = op_shape

  num_1s = 0
  while op_shape[-1] == 1 and new_sizes[-1] == 1:
    num_1s += 1
    op_shape = op_shape[:-1]
    new_sizes = new_sizes[:-1]

  i, j, count, out = 0, 0, 0, []
  while j < len(new_sizes):
    if op_shape[i] == new_sizes[j]:
      out.append(op_shape[i])
    else:
      count += 1
      if count > 1:
        raise ReshapeExplicitError()
      temp = [new_sizes[j]]
      next_j = j + 1
      next_i = i + 1
      while (math.prod(temp) != op_shape[i] or
             (next_j < len(new_sizes) and new_sizes[next_j] == 1)):
        if math.prod(temp) > op_shape[i]:
          return False, []
        if (math.prod(temp) == op_shape[i] and next_i < len(op_shape) and
            new_sizes[next_j] == op_shape[next_i]):
          break
        j += 1
        if j >= len(new_sizes):
          return False, []
        temp.append(new_sizes[j])
        next_j += 1
      out.append(temp)
    i += 1
    j += 1
  out.extend([1] * num_1s)

  assert len(orig_op_shape) == len(out)
  return True, out

