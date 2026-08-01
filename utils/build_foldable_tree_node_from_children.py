
def build_foldable_tree_node_from_children(
    prefix: RenderableTreePart | str,
    children: Sequence[RenderableAndLineAnnotations | RenderableTreePart | str],
    suffix: RenderableTreePart | str,
    comma_separated: bool = False,
    force_trailing_comma: bool = False,
    path: str | None = None,
    background_color: str | None = None,
    background_pattern: str | None = None,
    first_line_annotation: RenderableTreePart | None = None,
    expand_state: part_interface.ExpandState = (
        part_interface.ExpandState.WEAKLY_COLLAPSED
    ),
    *,
    child_type_single_and_plural: tuple[str, str] | None = None,
) -> RenderableAndLineAnnotations:
  """Builds a foldable tree node with path buttons.

  Args:
    prefix: Contents of the first line, before the children. Should not contain
      any other foldables. Usually ends with an opening paren/bracket, e.g.
      "SomeClass("
    children: Sequence of children of this node, which should each be rendered
      on their own line.
    suffix: Contents of the last line, after the children. Usually a closing
      paren/bracket for `prefix`.
    comma_separated: Whether to insert commas between children.
    force_trailing_comma: Whether to always insert a trailing comma after the
      last child.
    path: Keypath to this node from the root. If provided, copy-path buttons
      will be added.
    background_color: Optional background and border color for this node.
    background_pattern: Optional background pattern as a CSS "image". If
      provided, `background_color` must also be provided, and will be used as
      the border for the pattern.
    first_line_annotation: An annotation for the first line of the node when it
      is expanded.
    expand_state: Initial expand state for the foldable.
    child_type_single_and_plural: If provided, this will be used as the
      single and plural forms of the child type in the abbreviation.

  Returns:
    A new renderable part, possibly with a copy button annotation, for use
    in part of a rendered treescope tree.
  """
  if not children:
    return build_one_line_tree_node(
        line=basic_parts.siblings(prefix, suffix),
        path=path,
        background_color=background_color,
    )

  maybe_copy_button = build_copy_button(path)

  if isinstance(prefix, str):
    prefix = basic_parts.Text(prefix)

  if isinstance(suffix, str):
    suffix = basic_parts.Text(suffix)

  if background_pattern is not None:
    if background_color is None:
      raise ValueError(
          "background_color must be provided if background_pattern is"
      )

    def wrap_block(block):
      return common_styles.WithBlockPattern(
          block, color=background_color, pattern=background_pattern
      )

    wrap_topline = common_styles.PatternedTopLineSpanGroup
    wrap_bottomline = common_styles.PatternedBottomLineSpanGroup
    indented_child_class = common_styles.ColoredBorderIndentedChildren

  elif background_color is not None and background_color != "transparent":

    def wrap_block(block):
      return common_styles.WithBlockColor(block, color=background_color)

    wrap_topline = common_styles.ColoredTopLineSpanGroup
    wrap_bottomline = common_styles.ColoredBottomLineSpanGroup
    indented_child_class = common_styles.ColoredBorderIndentedChildren

  else:
    wrap_block = lambda rendering: rendering
    wrap_topline = lambda rendering: rendering
    wrap_bottomline = lambda rendering: rendering
    indented_child_class = basic_parts.IndentedChildren

  if first_line_annotation is not None:
    maybe_first_line_annotation = basic_parts.FoldCondition(
        expanded=first_line_annotation
    )
  else:
    maybe_first_line_annotation = basic_parts.EmptyPart()

  if child_type_single_and_plural:
    single, plural = child_type_single_and_plural
    if len(children) == 1:
      middle = f"1 {single}..."
    else:
      middle = f"{len(children)} {plural}..."
    abbreviation = basic_parts.siblings(
        common_styles.comment_color(basic_parts.text("<")),
        common_styles.abbreviation_color(basic_parts.text(middle)),
        common_styles.comment_color(basic_parts.text(">")),
    )
  else:
    abbreviation = None

  return RenderableAndLineAnnotations(
      renderable=wrap_block(
          foldable_impl.FoldableTreeNodeImpl(
              label=wrap_topline(prefix),
              contents=basic_parts.siblings(
                  maybe_copy_button,
                  maybe_first_line_annotation,
                  foldable_impl.abbreviatable(
                      foldable_impl.abbreviation_level(
                          indented_child_class.build(
                              children,
                              comma_separated=comma_separated,
                              force_trailing_comma=force_trailing_comma,
                          )
                      ),
                      abbreviation=abbreviation,
                  ),
                  wrap_bottomline(suffix),
              ),
              expand_state=expand_state,
          )
      ),
      annotations=maybe_copy_button,
  )

