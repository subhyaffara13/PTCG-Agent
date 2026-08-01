
def _process_mask(
    mask: mask_lib.MultiHeadMask,  # [num_heads, q_seq_len, kv_seq_len]
    block_shape: tuple[int, int],
    is_dkv: bool,
    *,
    downcast_smem_data: bool = True,
    head_shards: int = 1,
    q_seq_shards: int = 1,
    shrink_grid: bool = True,
) -> tuple[MaskInfo, jax_util.HashableFunction | None]:
  """Transform a dense mask into a sparse representation.

  The number of head and Q sequence shards are needed to create a MaskInfo
  object that is partitionable (with shmap or PartIR) along these two dimension.
  In particular for dKV MaskInfo, for each shard the indices of in the data_next
  array are relative to the current shard.
  The fwd and dQ MaskInfo objects do not change when sharding along the head or
  Q dimensions, they would be different if we were to shard along the KV
  dimension, but the kernel does not support that.

  Args:
    mask: Dense mask to process.
    block_shape: Shape of the Pallas grid block.
    is_dkv: True if we are processing the dKV mask
    downcast_smem_data: If True, downcast the scalar-memory data of MaskInfo to
      a data type smaller than np.int32 (if possible).
    head_shards: Number of head shards of the mesh in which the kernel is
      launched.
    q_seq_shards: Number of Q sequence shards of the mesh in which the kernel is
      launched.
    shrink_grid: Whether or not we should apply the grid shrinking optimization.

  Returns:
    `MaskInfo`, a sparse representation of the dense mask.
    `MaskCallable`: a callable that, given in input Q and KV indices, returns
      the value of the mask at those coordinates.

  Raises:
    ValueError: if the input mask is invalid or the block sizes are not
    compatible with the mask sizes.
  """

  if len(mask.shape) != 3:
    raise ValueError(f'Expected a 3-dim mask, instead got: {mask.shape=}')

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


  # Uniquify the masks.
  # Create a collection of the unique head masks in the input multi-head mask.
  # This avoids processing the same mask multiple times and it enables
  # deduplicating the partial mask blocks information.
  # Assign a unique ID to every unique mask.

  def assign_unique_ids(objects):
    id_map = collections.defaultdict(lambda: len(id_map))
    return {obj: id_map[obj] for obj in objects}

  unique_masks_dict: dict[mask_lib.Mask, int] = assign_unique_ids(
      head_mask for head_mask in mask.masks
  )

  # Build a mapping of heads to unique masks and masks to unique masks.

  head_to_mask_id: list[int] = [0] * head_count
  head_shard_to_mask_ids: list[set[int]] = [set() for _ in range(head_shards)]
  mask_id_to_heads: list[list[int]] = [
      [] for _ in range(len(unique_masks_dict))
  ]
  mask_id_to_head_shards: list[set[int]] = [
      set() for _ in range(len(unique_masks_dict))
  ]

  for head in range(head_count):
    mask_id = unique_masks_dict[mask.masks[head]]
    head_to_mask_id[head] = mask_id
    head_shard = head // heads_per_shard
    head_shard_to_mask_ids[head_shard].add(mask_id)
    mask_id_to_heads[mask_id].append(head)
    mask_id_to_head_shards[mask_id].add(head_shard)

  # If we have at most one unique mask per each head shard, then we can broadcast
  # the mask to all the heads in the shard. This is the common case.
  # If we have more than one mask in each head shard, then the optimization
  # cannot kick in and we use one mask for each head.
  # TODO(sharadmv,amagni): In the future we could think of a dynamic mapping of
  # heads to masks. This will likely introduce an additional field in the
  # MaskInfo class and runtime overhead to perform an indirect lookup. Since
  # having multiple masks per head-shard is not a common case we leave this for
  # future work.
  max_masks_per_head_shard = max(len(x) for x in head_shard_to_mask_ids)
  masks_per_head_shard = 1 if max_masks_per_head_shard == 1 else heads_per_shard

  unique_masks = [
      pair[0] for pair in sorted(unique_masks_dict.items(), key=lambda x: x[1])
  ]

  # TODO(amagni): checking the validity of the masks is slow for large masks.
  # Disable it for now, reevaluate in the future.

  partial_mask_block_ids: dict[_HashableNDArray, int] = collections.defaultdict(
      lambda: len(partial_mask_block_ids)
  )
  block_id_to_block_coords: dict[int, list[tuple[int, ...]]] = (
      collections.defaultdict(list)
  )

  # Shape of the block_mask, mask_next and data_next fields of MaskInfo.
  block_mask_shape = (
      head_shards if masks_per_head_shard == 1 else head_count,
      q_blocks_count,
      kv_blocks_count,
  )

  block_mask = np.zeros(block_mask_shape, dtype=np.int32)

  def set_block_mask(mask_id: int, q_index: int, kv_index: int, value: int):
    if masks_per_head_shard == 1:
      for shard_index in mask_id_to_head_shards[mask_id]:
        block_mask[shard_index, q_index, kv_index] = value
    else:
      for head_index in mask_id_to_heads[mask_id]:
        block_mask[head_index, q_index, kv_index] = value

  q_sequence = None
  mask_function = None
  if len(unique_masks) == 1:
    unique_mask = unique_masks[0]
    # The mask object either define q_sequence and mask_function or none of
    # them.
    assert hasattr(unique_mask, 'q_sequence') == hasattr(
        unique_mask, 'mask_function'
    )

    # If the mask object defines a q_sequence and a mask_function, then make use
    # of these in the kernel rather. This is preferable over loading the mask
    # from memory. When using a mask_function, then mask_next and
    # partial_mask_blocks are left undefined and not used in the kernel.
    if hasattr(unique_mask, 'q_sequence') and hasattr(
        unique_mask, 'mask_function'
    ):
      q_sequence = unique_mask.q_sequence
      mask_function = unique_mask.mask_function

  # Identify the partial mask blocks and the value of the block mask for each
  # block.
  # The partial mask blocks are "global", meaning it is a collection of such
  # blocks across all the heads. Partial mask blocks are uniquified.
  # When partitioning, all partial mask blocks are replicated across shards.
  # As a future extension we could assign to each head shard only the relevant
  # partial blocks. This would reduce the amount of data each shard needs
  # from: num_unique_partial_block_blocks to
  # max(unique_partial_blocks_per_shard)
  for mask_id, unique_mask in enumerate(unique_masks):
    for coords in np.ndindex((q_blocks_count, kv_blocks_count)):
      (q_index, kv_index) = coords
      chunk = unique_mask[(
          slice(q_index * q_block_size, (q_index + 1) * q_block_size),
          slice(kv_index * kv_block_size, (kv_index + 1) * kv_block_size),
      )]
      has_nonzero = chunk.any()
      if has_nonzero:
        all_nonzero = chunk.all()
        if not all_nonzero:
          set_block_mask(mask_id, q_index, kv_index, 1)
          partial_mask_block_id = partial_mask_block_ids[
              _HashableNDArray(chunk)
          ]
          for head_index in mask_id_to_heads[mask_id]:
            block_id_to_block_coords[partial_mask_block_id].append(
                (head_index,) + coords
            )
        else:
          set_block_mask(mask_id, q_index, kv_index, 2)

  unique_partial_mask_blocks = [
      pair[0]
      for pair in sorted(partial_mask_block_ids.items(), key=lambda x: x[1])
  ]

  # For each position in the in q, kv grid that contains a partial mask block
  # record the index of its partial mask block.
  coords_to_partial_mask_block_index = {}
  for partial_mask_block_id, coords in block_id_to_block_coords.items():
    for coo in coords:
      coords_to_partial_mask_block_index[coo] = partial_mask_block_id

  partial_mask_blocks = None
  has_mask_next = False
  if len(unique_partial_mask_blocks) >= 1:
    partial_mask_blocks = [x.array for x in unique_partial_mask_blocks]
    partial_mask_blocks = np.stack(partial_mask_blocks, axis=0).astype(np.bool_)
    has_mask_next = True
  if is_dkv and partial_mask_blocks is not None:
    partial_mask_blocks = np.swapaxes(partial_mask_blocks, -1, -2)

  all_head_shards_identical = all(
      head_shard_to_mask_ids[0] == x and len(x) == 1
      for x in head_shard_to_mask_ids
  )
  # When all the head shards are identical, we can process only one and
  # broadcast the result across all the head shards, this avoids redundant work.
  shards_to_process = 1 if all_head_shards_identical else head_shards

  # Iterate over the shards.
  # Work on a fraction of the mask at the time to compute the mask and the data
  # indices. This is needed to compute the correct data indices, which are
  # relative to the current slice of the mask.

  q_sequence_axis = 1
  head_axis = 0

  # Collect mask_info shards along the head dimension, concatenate (or
  # broadcast) them after the loop.
  data_next_per_head_list, mask_next_per_head_list = [], []
  for head_shard in range(shards_to_process):
    # Collect mask_info shards along the q_sequence dimension, concatenate them
    # after the loop.
    data_next_sequence_slices, mask_next_sequence_slices = [], []
    for q_seq_len_shard in range(q_seq_shards):
      head_start = head_shard * heads_per_shard
      q_seq_len_shard_size = q_blocks_per_shard * q_block_size
      q_seq_len_start = q_seq_len_shard * q_seq_len_shard_size

      blocked_q_seq_len_start = q_seq_len_shard * q_blocks_per_shard
      blocked_q_seq_len_slice = slice(
          blocked_q_seq_len_start,
          (q_seq_len_shard + 1) * q_blocks_per_shard,
      )

      if masks_per_head_shard == 1:
        unique_mask = unique_masks[head_to_mask_id[head_start]]
        unique_mask = mask_lib.MultiHeadMask((unique_mask,))
        current_mask = unique_mask
        mask_head_slice = slice(head_shard, head_shard + 1)
      else:
        current_mask = mask
        mask_head_slice = slice(head_start, (head_shard + 1) * heads_per_shard)

      # The current iteration of the loop processes a slice of the mask info
      # tensors of this shape:
      mask_info_slice_shape = (
          mask_head_slice.stop - mask_head_slice.start,
          blocked_q_seq_len_slice.stop - blocked_q_seq_len_slice.start,
          kv_blocks_count,
      )
      # Generate data_next and mask_next for the current slice.
      data_next_slice, mask_next_slice = _get_mask_info_for_shard(
          output_shape=mask_info_slice_shape,
          has_mask_next=has_mask_next,
          mask=current_mask,
          block_shape=block_shape,
          coords_to_partial_mask_block_index=coords_to_partial_mask_block_index,  # pyrefly: ignore[bad-argument-type]
          head_start=head_start,
          masks_per_head_shard=masks_per_head_shard,
          num_heads=1 if masks_per_head_shard == 1 else heads_per_shard,
          q_seq_start=q_seq_len_start,
          q_seq_shard_size=q_seq_len_shard_size,
          blocked_q_seq_start=blocked_q_seq_len_start,
          is_dkv=is_dkv,
      )
      data_next_sequence_slices.append(data_next_slice)
      mask_next_sequence_slices.append(mask_next_slice)

    # Concatenate the sequence shards.
    data_next_per_head = np.concatenate(
        data_next_sequence_slices, axis=q_sequence_axis
    )
    data_next_per_head_list.append(data_next_per_head)
    if has_mask_next:
      mask_next_per_head = np.concatenate(
          mask_next_sequence_slices, axis=q_sequence_axis
      )
      mask_next_per_head_list.append(mask_next_per_head)

  # Concatenate (or broadcast) the head shards.
  mask_next = None
  if all_head_shards_identical:
    assert len(data_next_per_head_list) == 1
    data_next_shard = data_next_per_head_list[0]
    assert data_next_shard.shape == (1, q_blocks_count, kv_blocks_count)
    data_next = np.broadcast_to(
        data_next_shard,
        (head_shards, q_blocks_count, kv_blocks_count),
    )
    if has_mask_next:
      assert len(mask_next_per_head_list) == 1
      mask_next_shard = mask_next_per_head_list[0]
      assert mask_next_shard.shape == (1, q_blocks_count, kv_blocks_count)
      mask_next = np.broadcast_to(
          mask_next_shard,
          (head_shards, q_blocks_count, kv_blocks_count),
      )
  else:
    data_next = np.concatenate(data_next_per_head_list, axis=head_axis)
    if has_mask_next:
      mask_next = np.concatenate(mask_next_per_head_list, axis=head_axis)

  # Shrink the width of the mask info when possible.
  if (
      shrink_grid
      and block_mask.shape[0] == head_shards
      and len(unique_masks) == 1
  ):
    rows_per_q_shard = block_mask.shape[1] // q_seq_shards
    block_mask_shards = []
    data_next_shards = []
    mask_next_shards = []

    # Slice the mask info arrays along the Q dimension. This simulates Q
    # sharding and enabled shrinking each Q shard of the MaskInfo arrays
    # independently.
    for q_seq_len_shard in range(q_seq_shards):
      rows = slice(
          q_seq_len_shard * rows_per_q_shard,
          (q_seq_len_shard + 1) * rows_per_q_shard,
      )
      current_block_mask = block_mask[:, rows, :]
      current_data_next = data_next[:, rows, :]
      current_mask_next = (
          mask_next[:, rows, :] if mask_next is not None else None
      )

      shrink_function = _shrink_mask_info_dkv if is_dkv else _shrink_mask_info

      current_block_mask, current_data_next, current_mask_next = (
          shrink_function(
              block_mask=current_block_mask,
              data_next=current_data_next,
              mask_next=current_mask_next,
              head_shards=head_shards,
          )
      )

      assert current_block_mask.size > 0
      assert current_data_next.size > 0
      assert current_mask_next is None or current_mask_next.size > 0
      assert current_block_mask.shape == current_data_next.shape
      assert (
          current_mask_next is None
          or current_block_mask.shape == current_mask_next.shape
      )

      block_mask_shards.append(current_block_mask)
      data_next_shards.append(current_data_next)
      mask_next_shards.append(current_mask_next)

    if q_seq_shards == 1:
      block_mask = block_mask_shards[0]
      data_next = data_next_shards[0]
      mask_next = mask_next_shards[0]
    else:
      # Since shrinking happens independently for each shard along Q we might
      # end up with uneven mask info shards. Insert padding where necessary to
      # maintain the SPMD paradigm.
      padding_axis = 1 if is_dkv else 2

      max_size = max(x.shape[padding_axis] for x in block_mask_shards)
      padded_block_mask_shards = []
      padded_data_next_shards = []
      padded_mask_next_shards = []
      assert (
          len(block_mask_shards)
          == len(data_next_shards)
          == len(mask_next_shards)
      )
      for (
          current_block_mask,
          current_data_next,
          current_mask_next,
      ) in zip(block_mask_shards, data_next_shards, mask_next_shards):
        # For dKV shrinking happens along axis Q (the rows of MaskInfo), for
        # fwd and dQ shrinking happens along axis KV (the columns of MaskInfo).
        if is_dkv:
          pad_width = (
              (0, 0),
              (0, max_size - current_block_mask.shape[padding_axis]),
              (0, 0),
          )
        else:
          pad_width = (
              (0, 0),
              (0, 0),
              (0, max_size - current_block_mask.shape[padding_axis]),
          )

        padded_block_mask_shards.append(
            np.pad(current_block_mask, pad_width=pad_width, constant_values=0)
        )
        # By padding data_next and mask_next with 'edge' policy we avoid
        # fetching new blocks thanks to 'immediate revisiting'.
        padded_data_next_shards.append(
            np.pad(current_data_next, pad_width=pad_width, mode='edge')
        )
        if current_mask_next is not None:
          padded_mask_next_shards.append(
              np.pad(current_mask_next, pad_width=pad_width, mode='edge')
          )

      block_mask = np.concatenate(padded_block_mask_shards, axis=1)
      data_next = np.concatenate(padded_data_next_shards, axis=1)
      mask_next = np.concatenate(padded_mask_next_shards, axis=1)

  if downcast_smem_data:
    data_next = _downcast_to_small_type(data_next)
    block_mask = _downcast_to_small_type(block_mask)
    if mask_next is not None:
      mask_next = _downcast_to_small_type(mask_next)

  assert (mask_function is not None) == (q_sequence is not None)
  # When the mask can be computed inside the kernel with a mask_function,
  # there is no need to load it from memory. So mask_next and
  # partial_mask_blocks are unused.
  return (
      MaskInfo(
          data_next=data_next,
          mask_next=mask_next if mask_function is None else None,
          block_mask=block_mask,
          partial_mask_blocks=partial_mask_blocks
          if mask_function is None
          else None,
          q_sequence=q_sequence,
      ),
      mask_function,
  )

