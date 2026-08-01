
def embedded_iframe(
    embedded_html: str,
    fallback_in_text_mode: RenderableTreePart,
    virtual_width: int = 80,
    virtual_height: int = 2,
) -> part_interface.RenderableTreePart:
  """Returns a wrapped child in a color for non-roundtrippable abbreviations."""
  if not isinstance(embedded_html, str):
    raise ValueError(
        '`embedded_html` must be a string, but got'
        f' {type(embedded_html).__name__}'
    )
  if not isinstance(fallback_in_text_mode, RenderableTreePart):
    raise ValueError(
        '`fallback_in_text_mode` must be a renderable part, but got'
        f' {type(fallback_in_text_mode).__name__}'
    )
  if not isinstance(virtual_width, int):
    raise ValueError(
        '`virtual_width` must be an integer, but got'
        f' {type(virtual_width).__name__}'
    )
  if not isinstance(virtual_height, int):
    raise ValueError(
        '`virtual_height` must be an integer, but got'
        f' {type(virtual_height).__name__}'
    )
  return EmbeddedIFrame(
      embedded_html=embedded_html,
      fallback_in_text_mode=fallback_in_text_mode,
      virtual_width=virtual_width,
      virtual_height=virtual_height,
  )

