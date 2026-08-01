
def render_enum(
    node: enum.Enum,
    path: str | None,
    subtree_renderer: renderers.TreescopeSubtreeRenderer,
) -> (
    rendering_parts.RenderableTreePart
    | rendering_parts.RenderableAndLineAnnotations
    | type(NotImplemented)
):
  """Renders an enum (roundtrippably, unlike the normal enum `repr`)."""
  del subtree_renderer
  cls = type(node)
  if node is getattr(cls, node.name):
    return rendering_parts.build_one_line_tree_node(
        rendering_parts.siblings_with_annotations(
            rendering_parts.maybe_qualified_type_name(cls),
            "." + node.name,
            extra_annotations=[
                rendering_parts.comment_color(
                    rendering_parts.text(f"  # value: {repr(node.value)}")
                )
            ],
        ),
        path,
    )
  else:
    return NotImplemented

