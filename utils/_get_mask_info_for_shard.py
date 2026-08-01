
def _get_mask_info_for_shard(
    output_shape: tuple[int, int, int],
    has_mask_next: bool,
    mask: mask_lib.MultiHeadMask | jax.Array,
    block_shape: tuple[int, int],
    coords_to_partial_mask_block_index: dict[tuple[int, int, int], int],
    masks_per_head_shard: int,
    head_start: int,
    num_heads: int,
    q_seq_start: int,
    q_seq_shard_size: int,
    blocked_q_seq_start: int,
    is_dkv: bool,
) -> tuple[np.ndarray, np.ndarray | None]:
  """Process a slice of the mask to compute data_next and mask_next.

  Args:
    output_shape: The shape of the data_next and mask_next to return
    has_mask_next: Whether mask_next should be constructed. If False None is
      returned for mask_next.
    mask: The full mask to be sliced according to the head and sequence ranges
    block_shape: Shape of the Pallas grid block.
    coords_to_partial_mask_block_index: Mapping between the pallas launch grid
      coordinates and the index of the corresponding block in partial mask block
      list.
    masks_per_head_shard: Number of masks per head shards
    head_start: First head of the current shard.
    num_heads: Number of heads in the shard.
    q_seq_start: Start index along the Q sequence for the current shard (in
      number of tokens).
    q_seq_shard_size: Number of tokens along the Q sequence for the current
      shard.
    blocked_q_seq_start: Start index along the Q sequence for the current shard
      (in number of grid blocks)
    is_dkv: True if we are processing the dKV mask

  Returns:
    Slice of data_next and mask_next (if required) that correspond to the
    current mask slice.
  """
  _, _, kv_seq_len = mask.shape

  q_block_size, kv_block_size = block_shape
  q_block_count, q_mod = divmod(q_seq_shard_size, q_block_size)
  kv_block_count, kv_mod = divmod(kv_seq_len, kv_block_size)

  assert q_mod == 0
  assert kv_mod == 0

  blocked_shape = (
      (kv_block_count, num_heads, q_block_count)
      if is_dkv
      else (num_heads, q_block_count, kv_block_count)
  )

  data_coords = []
  mask_coords = []
  for idx in np.ndindex(blocked_shape):
    if is_dkv:
      kv_index, h_index, q_index = idx
    else:
      h_index, q_index, kv_index = idx

    h_index = h_index if masks_per_head_shard == 1 else head_start + h_index

    chunk = mask[(
        h_index,
        slice(
            q_seq_start + q_index * q_block_size,
            q_seq_start + (q_index + 1) * q_block_size,
        ),
        slice(kv_index * kv_block_size, (kv_index + 1) * kv_block_size),
    )]
    if chunk.any():
      data_coords.append(idx)
      if not chunk.all():
        mask_coords.append(idx)

  # Initialize the output arrays.
  mask_next = None
  if has_mask_next:
    mask_next = np.zeros(output_shape, dtype=np.int32)
  data_next = np.zeros(output_shape, dtype=np.int32)

  # If the mask is completely zero'd out return freshly initialized outputs.
  if not data_coords:
    return data_next, mask_next

  data_coords_iter = iter(data_coords)
  first_j = coord_j = next(data_coords_iter)
  if mask_next is not None and mask_coords:
    mask_coords_iter = iter(mask_coords)
    first_m = coord_m = next(mask_coords_iter)
  else:
    first_m, coord_m, mask_coords_iter = None, None, None

  for idx in np.ndindex(blocked_shape):
    if is_dkv:
      kv_index, h_index, q_index = idx
      chunk_idx: tuple[int, ...] = (h_index, q_index, kv_index)
      data_dim = 2
    else:
      chunk_idx = idx
      data_dim = 2

    is_next = idx > coord_j

    if is_next:
      try:
        coord_j = next(data_coords_iter)
      except StopIteration:
        coord_j = first_j
    data_next[chunk_idx] = coord_j[data_dim]

    if mask_next is not None and mask_coords:
      assert coord_m is not None
      is_next_mask = idx > coord_m
      if is_next_mask:
        assert mask_coords_iter is not None
        try:
          coord_m = next(mask_coords_iter)
        except StopIteration:
          coord_m = first_m

      if is_dkv:
        assert coord_m is not None
        coord_m_global = (
            coord_m[1] + head_start,
            coord_m[2] + blocked_q_seq_start,
            coord_m[0],
        )
      else:
        assert coord_m is not None
        coord_m_global = (
            coord_m[0] + head_start,
            coord_m[1] + blocked_q_seq_start,
            coord_m[2],
        )

      mask_next[chunk_idx] = coords_to_partial_mask_block_index[coord_m_global]

  return data_next, mask_next

