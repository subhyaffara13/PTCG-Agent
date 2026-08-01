
def render_keyword(
    node: bool | None | type(Ellipsis) | type(NotImplemented),
    path: str | None,
    subtree_renderer: renderers.TreescopeSubtreeRenderer,
) -> (
    rendering_parts.RenderableTreePart
    | rendering_parts.RenderableAndLineAnnotations
    | type(NotImplemented)
):
  """Renders a builtin constant (None, False, True, ..., NotImplemented)."""
  del subtree_renderer
  return rendering_parts.build_one_line_tree_node(
      KeywordColor(rendering_parts.text(repr(node))), path
  )

