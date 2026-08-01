
def _extract_layout_candidates_from_broadcast(
    src: cs.RegisterLayout,
    dst: cs.Variable,
    dims: tuple[int, ...],
) -> Iterator[tuple[cs.Variable, cs.Constant]]:
  """Yields layout candidates for a broadcast equation."""
  match src.value:
    case fa.WGSplatFragLayout():
      yield dst, cs.RegisterLayout(fa.WGSplatFragLayout(dst.shape))
    case fa.WGStridedFragLayout() as src:
      dst_layout = fa.WGStridedFragLayout(dst.shape, src.vec_size)
      if fa.is_supported_strided_layout_broadcast(src, dst_layout, dims):
        yield dst, cs.RegisterLayout(dst_layout)

