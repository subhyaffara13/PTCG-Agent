
def build_one_line_tree_node(
    line: RenderableAndLineAnnotations | RenderableTreePart | str,
    path: str | None = None,
    background_color: str | None = None,
    background_pattern: str | None = None,
) -> RenderableAndLineAnnotations:
  """Builds a single-line tree node with path buttons.

  Args:
    line: Contents of the line.
    path: Keypath to this node from the root. If provided, copy-path buttons
      will be added.
    background_color: Optional background and border color for this node.
    background_pattern: Optional background pattern as a CSS "image". If
      provided, `background_color` must also be provided, and will be used as
      the border for the pattern.

  Returns:
    A new renderable part, possibly with a copy button annotation, for use
    in part of a rendered treescope tree.
  """
  maybe_copy_button = build_copy_button(path)

  if isinstance(line, RenderableAndLineAnnotations):
    line_primary = line.renderable
    annotations = basic_parts.siblings(maybe_copy_button, line.annotations)
  elif isinstance(line, str):
    line_primary = basic_parts.Text(line)
    annotations = maybe_copy_button
  else:
    line_primary = line
    annotations = maybe_copy_button

  if background_pattern is not None:
    if background_color is None:
      raise ValueError(
          "background_color must be provided if background_pattern is"
      )
    line_primary = common_styles.WithBlockPattern(
        common_styles.PatternedSingleLineSpanGroup(line_primary),
        color=background_color,
        pattern=background_pattern,
    )
  elif background_color is not None and background_color != "transparent":
    line_primary = common_styles.WithBlockColor(
        common_styles.ColoredSingleLineSpanGroup(line_primary),
        color=background_color,
    )

  return RenderableAndLineAnnotations(
      renderable=line_primary,
      annotations=annotations,
  )

