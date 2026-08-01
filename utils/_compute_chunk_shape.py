
def _compute_chunk_shape(
    local_shape: Sequence[int], dtype: str | jnp.dtype,
    file_size_target: int = _FILE_SIZE_TARGET) -> list[int]:
  """Compute a chunk such that it divides the local shape and is less than
  target file size. This helps the tensorstore kvstore driver limit the largest
  file size on disk to below the ``file_size_target``. We compute a chunk with a
  byte size at most 110% of the ``file_size_target``.
  """
  local_shape = list(local_shape)
  if len(local_shape) == 0 or math.prod(local_shape) == 0:
    # a zero size array needs a non-zero chunk passed to tensorstore for compat.
    return [max(z, 1) for z in local_shape]
  total_size = math.prod(local_shape) * jnp.dtype(dtype).itemsize
  axis_prime_factors = [_prime_factors(z) for z in local_shape]
  chunk_shape, chunk_size = list(local_shape), total_size
  # while chunk_size exceeds target size, reduce chunk_shape
  while chunk_size > 1.1 * file_size_target:  # 10% buffer
    # 1. find the smallest axis divisor across all axes
    chosen_axis_idx: int | None = None
    chosen_divisor = 1
    for axis_idx in range(len(chunk_shape)):
      if len(axis_prime_factors[axis_idx]) == 1:  # ignore axes sizes == 1
        continue
      if (chosen_axis_idx is None
          or chosen_divisor > axis_prime_factors[axis_idx][0]):
        chosen_axis_idx = axis_idx
        chosen_divisor = axis_prime_factors[axis_idx][0]
    # 2. if no divisor found, give up, return current chunk shape
    if chosen_axis_idx is None:
      return chunk_shape
    # 3. remove the applied divisor from prime factors
    prime_factors = axis_prime_factors[chosen_axis_idx]
    prime_factors.pop(0)
    # 4. apply the found divisor to reduce the chunk size
    chunk_shape[chosen_axis_idx] //= chosen_divisor
    chunk_size //= chosen_divisor
  return chunk_shape

