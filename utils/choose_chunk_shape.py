import logging
import math


def choose_chunk_shape(
    global_shape: Shape,
    write_shape: Shape,
    dtype: jnp.dtype | np.dtype,
    target_byte_size: int | None,
    *,
    shard_axes: tuple[int, ...] = (),
) -> Shape:
  """Chooses a chunk shape that divides the `write_shape`.

  The chunk shape is chosen such that the resulting byte size is less than
  or equal to `target_byte_size`, but is otherwise as large as possible.

  This uses a greedy algorithm that attempts to split the largest and sharded
  dimensions first, unless the `shard_axes` optional parameter is also provided.
  In the latter case, the algorithm will prioritize these explicitly specified
  axes and ensure that array's storage representation is sharded at least once
  on as many of these axes as possible.

  Args:
    global_shape: The global shape of the array.
    write_shape: The local shape being written.
    dtype: The dtype of the array.
    target_byte_size: Desired chunk byte size. Must be >= dtype.itemsize.
    shard_axes: [optional] A list of axes that should be prioritized for
      storage sharding. The implementation will try to shard at least once on as
      many of these axes as possible.

  Returns:
    List of length `len(write_shape)` specifying the chosen chunk shape.
  """
  if len(global_shape) != len(write_shape):
    raise ValueError(
        f'global_shape={global_shape} and write_shape={write_shape} must have'
        ' the same length.'
    )

  # TensorStore Zarr metadata doesn't support 0-sized dimensions.
  write_shape = tuple(max(1, d) for d in write_shape)

  if target_byte_size is None and not shard_axes:
    # No restrictions on chunk size or shape; return the write shape as-is.
    return write_shape

  sharded_dimensions = np.array(global_shape) != np.array(write_shape)
  dtype_size = dtype.itemsize
  rank = len(write_shape)

  # `dim_factors[i]` is the list of divisors of `write_shape[i]`
  # The current chunk shape is:
  #     [dim_factors[i][-1] for i in range(rank)]
  dim_factors = [_find_divisors(size) for size in write_shape]

  total_elements = math.prod(write_shape)

  def reduce_dim(dim_to_reduce: int) -> None:
    """Reduces the given dimension in the current chunk shape."""
    nonlocal total_elements
    current_dim = dim_factors[dim_to_reduce].pop()
    new_dim = dim_factors[dim_to_reduce][-1]
    total_elements = (total_elements // current_dim) * new_dim
    sharded_dimensions[dim_to_reduce] = True

  if any(axis < 0 or axis >= rank for axis in shard_axes):
    raise ValueError(
        f'All shard_axes={shard_axes} must be non-negative and less than'
        f' rank={rank}.'
    )

  # Reduce all explicitly requested shard axes.
  for shard_axis in shard_axes:
    while len(dim_factors[shard_axis]) > 1:
      reduce_dim(shard_axis)

  if target_byte_size is None:
    current_shape = tuple(dim_factors[i][-1] for i in range(rank))
    if current_shape != write_shape:
      logging.vlog(
          1,
          'Reduced write shape using shard_axes=%s only (no target_byte_size):'
          ' global_shape=%s, write_shape=%s, dtype=%s; reduced shape: %s',
          shard_axes,
          global_shape,
          write_shape,
          dtype,
          current_shape,
      )
    return current_shape

  # A target byte size is also specified. We will now try to find the smallest
  # chunk shape that satisfies the target byte size.

  # TODO: b/354139177 - This check is too generous; the minimally viable chunk
  # size should be set to something within the range of [4 KiB; 1 MiB] (from
  # TensorStore and storage performance considerations).
  if target_byte_size < dtype.itemsize:
    raise ValueError(
        f'target_byte_size={target_byte_size} must be >= {dtype.itemsize}'
    )

  if target_byte_size < 1 * _MIB:
    logging.warning(
        'Setting the target_byte_size too small could reduce performance.'
    )

  target_elements = target_byte_size // dtype_size

  # First, try to reduce the size of the chunk shape on axes that are already
  # sharded.
  could_shard = True
  while could_shard and total_elements > target_elements:
    could_shard = False
    # Find all dimensions that are sharded and can be sharded further.
    candidate_shard_dims = list(
        i
        for i in shard_axes
        if sharded_dimensions[i] and len(dim_factors[i]) > 1
    )
    # Shard once on each of the remaining dimensions in a round-robin fashion,
    # while we can.
    while candidate_shard_dims and total_elements > target_elements:
      could_shard = True
      # Find the minimum available divisor among the remaining dimensions.
      dim_idx = min(
          candidate_shard_dims,
          key=lambda i: dim_factors[i][-1] // dim_factors[i][-2],
      )
      reduce_dim(dim_idx)
      candidate_shard_dims.remove(dim_idx)

  # If we are not within target_byte_size yet, continue to reduce the current
  # chunk shape until the desired number of elements is reached.
  while total_elements > target_elements:
    # Greedily reduce the largest dimension.  This is not guaranteed to bring us
    # the closest to `target_elements`, but is simple to implement and should
    # work well enough.
    dim_to_reduce = -1
    dim_to_reduce_size = 1
    for i in range(rank):
      size = dim_factors[i][-1]
      if sharded_dimensions[i] and size > dim_to_reduce_size:
        dim_to_reduce_size = size
        dim_to_reduce = i

    if dim_to_reduce_size > 1:
      reduce_dim(dim_to_reduce)
    else:
      # We need to start splitting on unsharded dimensions.
      sharded_dimensions = np.ones(len(write_shape))

  chosen_shape = tuple(dim_factors[i][-1] for i in range(rank))

  # TODO: b/363218206 - Consider info logging the storage shape in saving and
  # loading code.
  logging.vlog(
      1,
      'Reduced write shape: global_shape=%s, write_shape=%s, dtype=%s,'
      ' target_byte_size=%d, shard_axes=%s; chosen shape: %s',
      global_shape,
      write_shape,
      dtype,
      target_byte_size,
      shard_axes,
      chosen_shape,
  )

  return chosen_shape

