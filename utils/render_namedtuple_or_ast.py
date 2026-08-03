from typing import Any

def render_namedtuple_or_ast(
    node: tuple[Any, ...] | ast.AST,
    path: str | None,
    subtree_renderer: renderers.TreescopeSubtreeRenderer,
) -> rendering_parts.RenderableAndLineAnnotations:
  """Renders a namedtuple or AST class."""
  ty = type(node)
  assert hasattr(ty, "_fields")
  return rendering_parts.build_foldable_tree_node_from_children(
      prefix=rendering_parts.siblings(
          rendering_parts.maybe_qualified_type_name(ty), "("
      ),
      children=rendering_parts.build_field_children(
          node, path, subtree_renderer, fields_or_attribute_names=ty._fields
      ),
      suffix=")",
      path=path,
      child_type_single_and_plural=("attribute", "attributes"),
  )

