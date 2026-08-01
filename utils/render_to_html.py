
def render_to_html(
    value: Any,
    roundtrip_mode: bool = False,
    ignore_exceptions: bool = False,
    compressed: bool = True,
) -> str:
  """Renders an object to HTML using the default renderer.

  Args:
    value: Value to render.
    roundtrip_mode: Whether to render in roundtrip mode.
    ignore_exceptions: Whether to catch errors during rendering of subtrees and
      show a fallback for those subtrees, instead of failing the entire
      renderer.
    compressed: Whether to compress the output HTML.

  Returns:
    HTML source code for the foldable representation of the object.
  """
  foldable_ir = rendering_parts.build_full_line_with_annotations(
      build_foldable_representation(value, ignore_exceptions=ignore_exceptions)
  )
  return lowering.render_to_html_as_root(
      foldable_ir, roundtrip_mode, compressed=compressed
  )

