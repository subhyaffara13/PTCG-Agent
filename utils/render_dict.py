
def render_dict(
    node: dict[Any, Any],
    path: str | None,
    subtree_renderer: renderers.TreescopeSubtreeRenderer,
) -> rendering_parts.RenderableAndLineAnnotations:
  """Renders a dictionary."""

  children = []
  for i, (key, child) in enumerate(node.items()):
    if i < len(node) - 1:
      # Not the last child. Always show a comma, and add a space when
      # collapsed.
      comma_after = rendering_parts.siblings(
          ",",
          rendering_parts.fold_condition(collapsed=rendering_parts.text(" ")),
      )
    else:
      # Last child: only show the comma when the node is expanded.
      comma_after = rendering_parts.fold_condition(
          expanded=rendering_parts.text(",")
      )

    child_path = None if path is None else f"{path}[{repr(key)}]"
    # Figure out whether this key is simple enough to render inline with
    # its value.
    key_rendering = subtree_renderer(key)
    value_rendering = subtree_renderer(child, path=child_path)

    if (
        key_rendering.renderable.collapsed_width < 40
        and not key_rendering.renderable.foldables_in_this_part()
        and key_rendering.annotations.collapsed_width == 0
    ):
      # Simple enough to render on one line.
      children.append(
          rendering_parts.siblings_with_annotations(
              key_rendering, ": ", value_rendering, comma_after
          )
      )
    else:
      # Should render on multiple lines.
      children.append(
          rendering_parts.siblings(
              rendering_parts.build_full_line_with_annotations(
                  key_rendering,
                  ":",
                  rendering_parts.fold_condition(
                      collapsed=rendering_parts.text(" ")
                  ),
              ),
              rendering_parts.indented_children([
                  rendering_parts.siblings_with_annotations(
                      value_rendering, comma_after
                  ),
                  rendering_parts.fold_condition(
                      expanded=rendering_parts.vertical_space("0.5em")
                  ),
              ]),
          )
      )

  if type(node) is dict:  # pylint: disable=unidiomatic-typecheck
    start = "{"
    end = "}"
  else:
    start = rendering_parts.siblings(
        rendering_parts.maybe_qualified_type_name(type(node)), "({"
    )
    end = "})"

  if not children:
    return rendering_parts.build_one_line_tree_node(
        line=rendering_parts.siblings(start, end), path=path
    )
  else:
    return rendering_parts.build_foldable_tree_node_from_children(
        prefix=start,
        children=children,
        suffix=end,
        path=path,
        child_type_single_and_plural=("item", "items"),
    )

