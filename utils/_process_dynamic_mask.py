import math


def _process_dynamic_mask(
    mask: jax.Array,
    block_shape: tuple[int, int],
    is_dkv: bool,
    *,
    downcast_smem_data: bool = True,
    head_shards: int = 1,
    q_seq_shards: int = 1,
    shrink_grid: bool = True,
) -> tuple[MaskInfo, None]:
  """Similar to `_process_mask` but the mask must be a dynamic array.

  Since the mask is dynamic, we can't know the exact number of partial mask
  blocks at trace time. Therefore, the entire mask is materialized in
  `partial_mask_blocks`.

  Note that we can still populate MaskInfo to skip fully-masked blocks.

  Args:
    mask: A [head_count, q_seq_len, kv_seq_len] jax.Array representing the dense
      mask to process.
    block_shape: A Tuple[int, int] representing the shape of the Pallas grid
      block.
    is_dkv: True if we are processing the dKV mask
    downcast_smem_data: If True, downcast the scalar-memory data of MaskInfo to
      a data type smaller than np.int32 (if possible).
    head_shards: Number of head shards of the mesh in which the kernel is
      launched.
    q_seq_shards: Number of Q sequence shards of the mesh in which the kernel is
      launched.
    shrink_grid: Whether or not we should apply the grid shrinking optimization.
      This is currently ignored.

  Returns:
    `MaskInfo`, a sparse representation of the dense mask.

  Raises:
    ValueError: if the input mask is invalid or the block sizes are not
    compatible with the mask sizes.
  """

  del shrink_grid
  if len(mask.shape) != 3:
    raise ValueError(f'Expected a 3-dim mask, instead got: {mask.shape}.')

  if mask.dtype != jnp.bool:
    raise ValueError(f'Expected a bool mask, instead got: {mask.dtype}.')

  head_count, q_seq_len, kv_seq_len = mask.shape
  q_block_size, kv_block_size = block_shape
  q_blocks_count, q_mod = divmod(q_seq_len, q_block_size)
  kv_blocks_count, kv_mod = divmod(kv_seq_len, kv_block_size)

  if q_mod != 0:
    raise ValueError(f'{q_block_size=} should divide {q_seq_len=}.')
  if kv_mod != 0:
    raise ValueError(f'{kv_block_size=} should divide {kv_seq_len=}.')

  q_seq_len_per_shard, mod = divmod(q_seq_len, q_seq_shards)
  if mod != 0:
    raise ValueError(f'{q_seq_shards=} should divide {q_seq_len=}.')

  q_blocks_per_shard, mod = divmod(q_seq_len_per_shard, q_block_size)
  if mod != 0:
    raise ValueError(f'{q_block_size=} should divide {q_seq_len_per_shard=}.')

  heads_per_shard, mod = divmod(head_count, head_shards)
  if mod != 0:
    raise ValueError(f'{head_shards=} should divide {head_count=}.')

  block_mask_shape = (
      head_count,
      q_blocks_count,
      kv_blocks_count,
  )

  # Tile the last 2 dimensions of the mask into 2D tiles of size `block_shape`.
  partial_mask_blocks = (
      mask.reshape(
          head_count,
          q_blocks_count,
          q_block_size,
          kv_blocks_count,
          kv_block_size,
      )
      .swapaxes(-2, -3)
      .astype(np.bool_)
  )

  # The block mask is 2 for all blocks with all entries set to True and 1 for
  # blocks with a mix of True and False entries.
  is_full_mask = jnp.all(partial_mask_blocks, axis=(-1, -2))
  is_empty_mask = jnp.logical_not(jnp.any(partial_mask_blocks, axis=(-1, -2)))

  block_mask = jnp.ones(block_mask_shape, dtype=np.int32)
  block_mask = jnp.where(is_full_mask, 2, block_mask)
  block_mask = jnp.where(is_empty_mask, 0, block_mask)

  q_sequence_axis = 1
  head_axis = 0

  # Each iteration of the loop processes a slice of the mask info
  # tensors of this shape:
  mask_info_slice_shape = (heads_per_shard, q_blocks_per_shard, kv_blocks_count)

  # Collect mask_info shards along the head dimension, concatenate (or
  # broadcast) them after the loop.
  data_next_per_head_list, mask_next_per_head_list = [], []
  for head_shard in range(head_shards):
    head_start = head_shard * heads_per_shard
    mask_head_slice = slice(head_start, head_start + heads_per_shard)

    # Collect mask_info shards along the q_sequence dimension, concatenate them
    # after the loop.
    data_next_sequence_slices, mask_next_sequence_slices = [], []
    for q_seq_len_shard in range(q_seq_shards):
      q_seq_len_start = q_seq_len_shard * q_blocks_per_shard
      blocked_q_seq_len_slice = slice(
          q_seq_len_start, q_seq_len_start + q_blocks_per_shard
      )
      local_block_mask = block_mask[mask_head_slice, blocked_q_seq_len_slice]

      mask_next_slice = jnp.arange(
          math.prod(mask_info_slice_shape), dtype=np.int32
      ).reshape(mask_info_slice_shape)
      mask_next_slice = jnp.where(local_block_mask == 1, mask_next_slice, 0)

      # data_next stores the index of the next non-empty data block in the sequence.
      # The indices of empty blocks are set to 0 to avoid copying extra data when
      # pipeling.
      if is_dkv:
        data_next_slice = jnp.arange(q_blocks_per_shard, dtype=np.int32)[
            None, :, None
        ]
      else:
        data_next_slice = jnp.arange(kv_blocks_count, dtype=np.int32)[
            None, None, :
        ]
      data_next_slice = jnp.broadcast_to(data_next_slice, mask_info_slice_shape)
      data_next_slice = jnp.where(local_block_mask == 0, 0, data_next_slice)

      data_next_sequence_slices.append(data_next_slice)
      mask_next_sequence_slices.append(mask_next_slice)

    # Concatenate the sequence shards.
    data_next_per_head = jnp.concatenate(
        data_next_sequence_slices, axis=q_sequence_axis
    )
    data_next_per_head_list.append(data_next_per_head)
    mask_next_per_head = jnp.concatenate(
        mask_next_sequence_slices, axis=q_sequence_axis
    )
    mask_next_per_head_list.append(mask_next_per_head)

  # Concatenate (or broadcast) the head shards.
  data_next = jnp.concatenate(data_next_per_head_list, axis=head_axis)
  mask_next = jnp.concatenate(mask_next_per_head_list, axis=head_axis)

  if is_dkv:
    partial_mask_blocks = partial_mask_blocks.swapaxes(-1, -2)

  def _downcast(array: jax.Array, max_value: int) -> jax.Array:
    if array.size == 0:
      return array

    if array.dtype != np.int32:
      raise ValueError(f'Expected int32 input, but got {array.dtype}.')

    if max_value <= np.iinfo(np.int8).max:
      return array.astype(np.int8)
    elif max_value <= np.iinfo(np.int16).max:
      return array.astype(np.int16)
    else:
      return array.astype(np.int32)

  if downcast_smem_data:
    block_mask = block_mask.astype(np.int8)  # values are in the range [0, 1, 2]
    data_next = _downcast(
        data_next, q_blocks_per_shard if is_dkv else kv_blocks_count
    )
    mask_next = _downcast(
        mask_next, heads_per_shard * q_blocks_per_shard * kv_blocks_count
    )

  return (
      MaskInfo(
          data_next=data_next,
          mask_next=mask_next,
          block_mask=block_mask,
          partial_mask_blocks=partial_mask_blocks,
          q_sequence=None,
          is_dynamic_mask=True,
      ),
      None,
  )

