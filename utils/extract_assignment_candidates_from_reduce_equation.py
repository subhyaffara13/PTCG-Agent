
def extract_assignment_candidates_from_reduce_equation(
    small: cs.RegisterLayout,
    large: cs.Variable,
    reduction_dims: tuple[int, ...],
    keep_dims: bool,
) -> Iterator[cs.RegisterLayout]:
  """Yields layout candidates for the reduce equation `small = reduce(large, reduction_dims)."""
  large_shape = large.shape

  if isinstance(small.value, fa.WGSplatFragLayout):
    yield cs.RegisterLayout(fa.WGSplatFragLayout(large_shape))
    return

  if isinstance(small.value, fa.WGStridedFragLayout):
    layout = fa.WGStridedFragLayout(large_shape, small.value.vec_size)
    yield cs.RegisterLayout(layout)
    return

  assert isinstance(small.value, fa.TiledLayout)
  # TODO(allanrenucci): Add support for reducing tiled layouts when keep_dims=True.
  if keep_dims:
    return

  candidates = [
      fa.WGMMA_LAYOUT,
      fa.WGMMA_TRANSPOSED_LAYOUT,
      fa.TCGEN05_LAYOUT,
      fa.TCGEN05_TRANSPOSED_LAYOUT,
      tcgen05.TMEM_NATIVE_LAYOUT,
  ]
  if large_shape[-1] % 16 == 0:
    candidates.append(tcgen05.fa_m64_collective_layout(large_shape[-1]))

  # In the case where we are not actually reducing any of the tiled dimensions,
  # we should consider the "small" layout as a candidate. We consider it last,
  # since it is always a valid assignment when reducing a leading tiled
  # dimension. Using it as a candidate early makes no theoretical difference,
  # but it practice could lead to longer-winded backtracking.
  candidates.append(small.value)

  for candidate in candidates:
    if len(candidate.base_tile_shape) > len(large_shape):
      continue
    num_untiled_dims = len(large_shape) - len(candidate.base_tile_shape)
    reduced_tiling_axes = tuple(
        a - num_untiled_dims for a in reduction_dims if a >= num_untiled_dims
    )
    if candidate.reduce(reduced_tiling_axes) == small.value:
      yield cs.RegisterLayout(candidate)

