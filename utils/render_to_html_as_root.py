
def render_to_html_as_root(
    root_node: rendering_parts.RenderableTreePart,
    roundtrip: bool = False,
    compressed: bool = False,
) -> str:
  """Renders a root node to HTML.

  This handles collecting styles and JS definitions and inserting the root
  HTML element.

  Args:
    root_node: The root node to render.
    roundtrip: Whether to render in roundtrip mode.
    compressed: Whether to compress the HTML for display.

  Returns:
    HTML source for the rendered node.
  """
  render_iterator = _render_to_html_as_root_streaming(root_node, roundtrip, [])
  html_src = "".join(render_iterator)
  return html_encapsulation.encapsulate_html(html_src, compress=compressed)

