
def handle_code_objects_with_reflection(
    node: Any,
    path: str | None,
    subtree_renderer: renderers.TreescopeSubtreeRenderer,
    show_closure_vars: bool = False,
) -> (
    rendering_parts.RenderableTreePart
    | rendering_parts.RenderableAndLineAnnotations
    | type(NotImplemented)
):
  """Renders code objects using reflection and closure inspection."""
  if inspect.isclass(node):
    # Render class.
    closure_vars = None
  elif inspect.isfunction(node):
    # Render function.
    if show_closure_vars:
      closure_vars = inspect.getclosurevars(node).nonlocals
    else:
      closure_vars = None
  else:
    # Not a supported object.
    return NotImplemented

  annotations = []
  filepath, lineno = _get_filepath_and_lineno(node)
  if filepath is not None:
    annotations.append(
        rendering_parts.comment_color(
            rendering_parts.siblings(
                rendering_parts.text("  # Defined at "),
                format_source_location(filepath, lineno),
            )
        )
    )

  if closure_vars:
    boxed_closure_var_rendering = rendering_parts.in_outlined_box(
        rendering_parts.on_separate_lines([
            rendering_parts.comment_color(
                rendering_parts.text("# Closure variables:")
            ),
            subtree_renderer(closure_vars),
        ])
    )
    return rendering_parts.siblings_with_annotations(
        rendering_parts.build_custom_foldable_tree_node(
            label=rendering_parts.abbreviation_color(
                rendering_parts.text(repr(node))
            ),
            contents=rendering_parts.fold_condition(
                expanded=rendering_parts.indented_children(
                    [boxed_closure_var_rendering]
                )
            ),
            path=path,
        ),
        extra_annotations=annotations,
    )

  else:
    return rendering_parts.siblings_with_annotations(
        rendering_parts.build_one_line_tree_node(
            line=rendering_parts.abbreviation_color(
                rendering_parts.text(repr(node))
            ),
            path=path,
        ),
        extra_annotations=annotations,
    )

