from typing import Any

def handle_basic_types(
    node: Any,
    path: str | None,
    subtree_renderer: renderers.TreescopeSubtreeRenderer,
) -> (
    rendering_parts.RenderableTreePart
    | rendering_parts.RenderableAndLineAnnotations
    | type(NotImplemented)
):
  """Renders basic builtin Python types."""
  candidate_type = type(node)
  for supertype in candidate_type.__mro__:
    if supertype in BUILTINS_REGISTRY:
      return BUILTINS_REGISTRY[supertype](node, path, subtree_renderer)

  if dataclasses.is_dataclass(node) and not isinstance(node, type):
    constructor_open = rendering_parts.render_dataclass_constructor(node)
    if hasattr(node, "__treescope_color__") and callable(
        node.__treescope_color__
    ):
      background_color, background_pattern = (
          formatting_util.parse_simple_color_and_pattern_spec(
              node.__treescope_color__(), type(node).__name__
          )
      )
    else:
      background_color = None
      background_pattern = None

    return rendering_parts.build_foldable_tree_node_from_children(
        prefix=constructor_open,
        children=rendering_parts.build_field_children(
            node,
            path,
            subtree_renderer,
            fields_or_attribute_names=dataclasses.fields(node),
        ),
        suffix=")",
        path=path,
        background_color=background_color,
        background_pattern=background_pattern,
        child_type_single_and_plural=("field", "fields"),
    )

  return NotImplemented

