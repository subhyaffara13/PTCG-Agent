
def compute_scalar_offset(iteration_index,
                          total_size: Shape,
                          block_size: Shape):
  ndims = len(iteration_index)
  dim_size = 1
  total_idx = 0
  for i in range(ndims-1, -1, -1):
    dim_idx = iteration_index[i] * block_size[i]
    total_idx += dim_idx * dim_size
    dim_size *= total_size[i]
  return total_idx

