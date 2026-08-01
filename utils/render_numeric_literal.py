
def render_numeric_literal(
    node: int | float,
    path: str | None,
    subtree_renderer: renderers.TreescopeSubtreeRenderer,
) -> (
    rendering_parts.RenderableTreePart
    | rendering_parts.RenderableAndLineAnnotations
    | type(NotImplemented)
):
  """Renders a numeric literal."""
  del subtree_renderer
  return rendering_parts.build_one_line_tree_node(
      NumberColor(rendering_parts.text(repr(node))), path
  )

