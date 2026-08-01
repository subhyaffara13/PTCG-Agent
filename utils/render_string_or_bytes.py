
def render_string_or_bytes(
    node: str | bytes,
    path: str | None,
    subtree_renderer: renderers.TreescopeSubtreeRenderer,
) -> (
    rendering_parts.RenderableTreePart
    | rendering_parts.RenderableAndLineAnnotations
    | type(NotImplemented)
):
  """Renders a string or bytes literal."""
  del subtree_renderer
  lines = node.splitlines(keepends=True)
  if len(lines) > 1:
    # For multiline strings, we use two renderings:
    # - When collapsed, they render with ordinary `repr`,
    # - When expanded, they render as the implicit concatenation of per-line
    #   string literals.
    # Note that the `repr` for a string sometimes switches delimiters
    # depending on whether the string contains quotes or not, so we can't do
    # much manipulation of the strings themselves. This means that the safest
    # thing to do is to just embed two copies of the string into the IR,
    # one for the full string and the other for each line.
    result = rendering_parts.build_custom_foldable_tree_node(
        contents=StringLiteralColor(
            rendering_parts.fold_condition(
                collapsed=rendering_parts.text(repr(node)),
                expanded=rendering_parts.indented_children(
                    children=[
                        rendering_parts.text(repr(line)) for line in lines
                    ],
                    comma_separated=False,
                ),
            )
        ),
        path=path,
    )
  else:
    # No newlines, so render it on a single line.
    result = rendering_parts.build_one_line_tree_node(
        StringLiteralColor(rendering_parts.text(repr(node))), path
    )
  # Abbreviate long strings.
  if len(node) > 20:
    remaining = len(node) - 10
    result = foldable_impl.abbreviatable_with_annotations(
        result,
        abbreviation=basic_parts.siblings(
            StringLiteralColor(rendering_parts.text(repr(node[:5]))),
            common_styles.abbreviation_color(
                rendering_parts.text(f"<{remaining} chars...>")
            ),
            StringLiteralColor(rendering_parts.text(repr(node[-5:]))),
        ),
    )
  return result

