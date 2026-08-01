
def _is_supported_tiled_relayout(
    src: fa.TiledLayout, dst: fa.TiledLayout, bitwidth: int
) -> bool:
  """Returns whether the source->target relayout is supported for values of types with the given bitwidth."""
  match src, dst:
    # Transposed layouts.
    case fa.WGMMA_LAYOUT, fa.WGMMA_TRANSPOSED_LAYOUT:
      return True
    case fa.WGMMA_TRANSPOSED_LAYOUT, fa.WGMMA_LAYOUT:
      return True
    case fa.TCGEN05_LAYOUT, fa.TCGEN05_TRANSPOSED_LAYOUT:
      return True
    case fa.TCGEN05_TRANSPOSED_LAYOUT, fa.TCGEN05_LAYOUT:
      return True
    # "Conversion-optimized" layouts.
    case fa.WGMMA_LAYOUT_UPCAST_2X, fa.WGMMA_LAYOUT:
      return fa.can_relayout_wgmma_2x_to_wgmma(bitwidth)
    case fa.WGMMA_LAYOUT_UPCAST_4X, fa.WGMMA_LAYOUT_UPCAST_2X:
      return fa.can_relayout_wgmma_4x_to_wgmma_2x(bitwidth)
    case fa.WGMMA_LAYOUT_UPCAST_4X, fa.WGMMA_LAYOUT:
      return fa.can_relayout_wgmma_4x_to_wgmma_2x(
          bitwidth
      ) and fa.can_relayout_wgmma_2x_to_wgmma(bitwidth)
  if src == fa.tmem_native_layout(
      src.vector_length
  ) and dst == fa.tmem_native_layout(dst.vector_length):
    return True
  return False

