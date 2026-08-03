import itertools
import math


def plan_tiled_transfer(
    nested_ref_shape: Sequence[Sequence[int]],
    nested_ref_strides: Sequence[Sequence[int]],
    layout: TiledLayout,
    element_bits: int,
    swizzle: int,
) -> TransferPlan:
  """Plans the tiled transfer in a way that avoids SMEM bank conflicts.

  Arguments:
    nested_ref_shape: The nested shape of the reference. For a logical ref with
      shape (2, 8, 16) and tiling (2, 8), this would be ((2,), (4, 2), (2, 8)).
    nested_ref_strides: The strides associated with the `nested_ref_shape`.
    layout: The layout of the value in registers being transferred.
    element_bits: Element bitwidth.
    swizzle: The swizzle pattern length.
  """
  tiling = layout.tiling
  tiled_nested_shape, tiled_nested_strides = tiling.tile_nested_shape_strides(
      tuple(tuple(x) for x in nested_ref_shape),
      tuple(tuple(x) for x in nested_ref_strides),
  )

  tiles_shape = list(tiled_nested_shape)
  tiles_strides = list(tiled_nested_strides)
  for d in (*layout.partitioned_warp_dims, *layout.partitioned_lane_dims, layout.vector_dim):
    tiles_shape[d] = (1,) * len(tiles_shape[d])
    tiles_strides[d] = (0,) * len(tiles_strides[d])
  tiles_shape = list(itertools.chain.from_iterable(tiles_shape))
  tiles_strides = list(itertools.chain.from_iterable(tiles_strides))

  warp_shape = list(itertools.chain.from_iterable(
      (d.times,) if isinstance(d, Replicated) else tiled_nested_shape[d] for d in layout.warp_dims
  ))
  warp_strides = list(itertools.chain.from_iterable(
      (0,) if isinstance(d, Replicated) else tiled_nested_strides[d] for d in layout.warp_dims
  ))
  lane_shape = list(itertools.chain.from_iterable(
      (d.times,) if isinstance(d, Replicated) else tiled_nested_shape[d] for d in layout.lane_dims
  ))
  lane_strides = list(itertools.chain.from_iterable(
      (0,) if isinstance(d, Replicated) else tiled_nested_strides[d] for d in layout.lane_dims
  ))
  vector_length = layout.vector_length
  # TODO(apaszke): Rewrite this function in terms of transfer_bytes (that we get
  # from the caller).
  swizzle_tile_elems = (16 * 8) // element_bits
  swizzle_group_elems = (128 * 8) // element_bits
  # Should be checked at the call site.
  assert vector_length * element_bits % 8 == 0
  transfer_bytes = (vector_length * element_bits) // 8
  # Below, all calculations are in elements, not in bytes, since it should
  # generalize better to sub-byte types.
  # Here, we verify two conditions:
  # 1. Each vector transfer only accesses addresses that fall within a single
  # swizzle tile (if not we'd need to split it and swizzle parts differently).
  chain = itertools.chain
  transfer_alignment = math.gcd(*(
      s
      for (s, d) in zip(
          chain(tiles_strides, warp_strides, lane_strides),
          chain(tiles_shape, warp_shape, lane_shape),
      )
      if d > 1
  ))
  if (
      swizzle_tile_elems % transfer_alignment
      and vector_length <= transfer_alignment
  ):
    raise TransferPlanDerivationError(
        "Failed to prove that vector transfers don't cross swizzle tile"
        " boundaries. This check is incomplete, and does not guarantee that"
        f" this is a user error, but it might be. {transfer_alignment=}"
    )

  # 2. The transfer pattern does not cause bank conflicts.
  # TODO(apaszke): For now, when performing transfers narrower than a bank,
  # we simply narrow each bank to the transfer width. The truth is more likely
  # that bank conflicts only don't occur if the addresses mapping to the same
  # bank are contiguous, but that's a more complicated check to perform.
  if transfer_bytes > SMEM_BANK_BYTES * 4:
    raise TransferPlanDerivationError(
        f"{transfer_bytes=} > {SMEM_BANK_BYTES * 4} not implemented"
    )
  if element_bits > SMEM_BANK_BYTES * 8:
    raise TransferPlanDerivationError(
        f"{element_bits=} > {SMEM_BANK_BYTES * 8} not implemented"
    )
  smem_bank_bytes = min(SMEM_BANK_BYTES, transfer_bytes)
  num_banks = SMEM_BANKS * (SMEM_BANK_BYTES // smem_bank_bytes)
  elems_per_bank = (smem_bank_bytes * 8) // element_bits
  num_wavefronts = max(transfer_bytes // smem_bank_bytes, 1)
  wavefront_lanes = WARP_SIZE // num_wavefronts

  lane_mask = np.full(lane_shape, False)
  lane_mask[tuple(slice(0, 1) if s == 0 else slice(None) for s in lane_strides)] = True
  wavefront_mask = lane_mask.reshape(num_wavefronts, wavefront_lanes)

  lane_offsets_in_tile = np.dot(list(np.ndindex(*lane_shape)), lane_strides)
  def has_bank_conflicts(tile_idx_transform):
    num_tiles = math.prod(tiles_shape)
    tile_idxs = np.unravel_index(np.arange(num_tiles), tiles_shape)
    tile_idxs = np.expand_dims(np.stack(tile_idxs, 1), 1)  # [#tiles, 1, #dims]
    lane_tile_idx = tile_idx_transform(tile_idxs)  # [#tiles, #lanes/1, #dims]
    assert lane_tile_idx.shape[1] in {1, WARP_SIZE}
    lane_tile_offsets = np.dot(lane_tile_idx, tiles_strides)
    offsets = lane_tile_offsets + lane_offsets_in_tile  # [#tiles, #lanes]
    assert offsets.shape[-1] == WARP_SIZE
    swizzle_groups = (offsets // swizzle_group_elems) % (swizzle // 16)
    swizzle_bits = swizzle_groups * swizzle_tile_elems
    lane_banks = ((offsets ^ swizzle_bits) // elems_per_bank) % num_banks
    wavefront_banks = lane_banks.reshape(-1, num_wavefronts, wavefront_lanes)
    # We step over wavefronts since they might have a different number of lanes.
    wavefront_banks = wavefront_banks.swapaxes(0, 1)
    for banks, mask in zip(wavefront_banks, wavefront_mask):
      banks = banks[:, mask]
      # Order of threads within the wavefront is unimportant.
      banks = np.sort(banks, axis=-1)
      # There are no conflicts if each wavefront only contains unique banks.
      repeats = np.any(banks[..., 1:] == banks[..., :-1])
      if repeats:
        return True
    return False

  # We don't need any special treatment if there are no conflicts when each lane
  # transfers the same tile at a time.
  if not has_bank_conflicts(lambda tile_idx: tile_idx):
    return TrivialTransferPlan()

  # Otherwise, we will try to partition the lanes into two groups and have
  # each group store to different tile. The only tile dimensions that can help
  # us with bank conflicts are those that have multiple elements and a stride
  # that's not a multiple of the number of banks.
  #
  # Note that the code is set up so that we could also consider partitioning
  # the lanes into more groups, but the selects will become more expensive if
  # we do that. It's a possibility we have if we need it.
  candidate_dims = (
      i for i, (s, d) in enumerate(zip(tiles_strides, tiles_shape))
      if d > 1 and s % (SMEM_BANKS * elems_per_bank)
  )
  for dim in candidate_dims:
    for group_stride in (1, 2, 4, 8, 16):
      # We change the group assignment each group_stride lanes.
      lane_id = np.arange(WARP_SIZE)[:, None]
      lane_group = (lane_id // group_stride) % 2
      # We only consider a transformation where the second group stores to a
      # tile that's a constant offset (modulo dim size) from the first one.
      for stagger in range(1, tiles_shape[dim]):
        offset = np.zeros(len(tiles_shape), np.int64)
        offset[dim] = stagger
        transform = lambda idx: (idx + offset * lane_group) % tiles_shape
        if not has_bank_conflicts(transform):
          # We've found a strategy that avoids bank conflicts!
          return StaggeredTransferPlan(
              stagger, dim, tiles_shape[dim], group_stride
          )
  raise TransferPlanDerivationError(
      "Failed to synthesize a transfer pattern that avoids bank conflicts"
  )

