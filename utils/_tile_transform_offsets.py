
def _tile_transform_offsets(
    tiling: Sequence[int],
    static_offsets: Sequence[int],
    dynamic_offsets: Sequence[ir.Value],
) -> tuple[Sequence[int], Sequence[ir.Value]]:
  """Computes the static and dynamic offsets after the given tiling is applied.

  Conceptually, this function is analogous to
  tile.transform_shape(static_offsets), except that it also handles dynamic offsets.
  """
  dynamic_offset_index = 0
  new_static_offsets = []
  new_dynamic_offsets = []

  # Preserve all offsets in non-tiled dimensions.
  for offset in static_offsets[: -len(tiling)]:
    new_static_offsets.append(offset)
    if offset == ir.ShapedType.get_dynamic_stride_or_offset():
      new_dynamic_offsets.append(dynamic_offsets[dynamic_offset_index])
      dynamic_offset_index += 1

  # Compute static and dynamic offsets of tiled dimensions.
  for tile_size, offset in zip(
      tiling, static_offsets[-len(tiling) :], strict=True
  ):
    if offset == ir.ShapedType.get_dynamic_stride_or_offset():
      # Here we assume that the offset is divisble by the tile size, but we
      # don't check it. This has been established at the time the tiling was
      # inferred.
      dyn_offset = arith.divui(
          dynamic_offsets[dynamic_offset_index],
          utils.c(tile_size, ir.IndexType.get()),
      )
      new_dynamic_offsets.append(dyn_offset)
      new_static_offsets.append(ir.ShapedType.get_dynamic_stride_or_offset())
      dynamic_offset_index += 1
    else:
      assert offset % tile_size == 0
      new_static_offsets.append(offset // tile_size)

  # Add 0 offsets for the newly created dimension of the tile.
  new_static_offsets += [0] * len(tiling)

  return new_static_offsets, new_dynamic_offsets

