
def render_simplenamespace(
    node: types.SimpleNamespace,
    path: str | None,
    subtree_renderer: renderers.TreescopeSubtreeRenderer,
) -> rendering_parts.RenderableAndLineAnnotations:
  """Renders a SimpleNamespace."""
  return rendering_parts.build_foldable_tree_node_from_children(
      prefix=rendering_parts.siblings(
          rendering_parts.maybe_qualified_type_name(type(node)), "("
      ),
      children=rendering_parts.build_field_children(
          node,
          path,
          subtree_renderer,
          fields_or_attribute_names=tuple(node.__dict__.keys()),
      ),
      suffix=")",
      path=path,
      child_type_single_and_plural=("attribute", "attributes"),
  )

