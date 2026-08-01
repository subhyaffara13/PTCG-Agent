
def _register_layouts_for_optimized_transfer_to_smem(
    shaped_type: ir.ShapedType,
    smem_layout: cs.SMEMTransforms,
    arch: tuple[int, int],
) -> Iterator[fa.FragmentedLayout]:
  """Yields register layout candidates for optimized transfers to SMEM."""
  if smem_layout.tiling is None:
    reg_layout = fa.WGStridedFragLayout.from_shaped_type(shaped_type)
    if reg_layout is not None:
      yield reg_layout
    return

  if is_hopper(arch):
    candidate_layouts = [
        fa.WGMMA_LAYOUT,
        fa.WGMMA_TRANSPOSED_LAYOUT,
    ]
  else:
    # For now, just assume that if it's not Hopper, it's Blackwell.
    candidate_layouts = [
        # Try the layouts with larger base tiles first.
        fa.TCGEN05_LAYOUT,
        fa.TCGEN05_TRANSPOSED_LAYOUT,
        # Keep using WGMMA and WGMMA_TRANSPOSED layouts here, simply because
        # they may apply to smaller shapes where TCGEN05 layouts do not apply.
        # This can be useful for kernels not involving MMAs that still need
        # optimized transfers to TiledLayouts, and actually shows up in some
        # tests.
        fa.WGMMA_LAYOUT,
        fa.WGMMA_TRANSPOSED_LAYOUT,
    ]

  yield from candidate_layouts

